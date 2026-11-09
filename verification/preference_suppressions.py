"""Locate qualified source symbols and their prescribed suppression comments."""

import ast
import io
import re
import tokenize

from verification.preference_proofs import PreferenceCheckError


def definitions(source: str) -> dict[str, tuple[int, int, str]]:
    """Record qualified class and function extents without executing source."""
    result: dict[str, tuple[int, int, str]] = {}

    def visit(node: ast.AST, prefix: str) -> None:
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                name = prefix + child.name
                if name in result or child.end_lineno is None:
                    raise PreferenceCheckError("ambiguous_symbol")
                kind = "function"
                if isinstance(child, ast.ClassDef):
                    kind = (
                        "test"
                        if any(
                            ast.unparse(base) == "unittest.TestCase"
                            for base in child.bases
                        )
                        else "class"
                    )
                result[name] = (child.lineno, child.end_lineno, kind)
                visit(child, name + ".")
            else:
                visit(child, prefix)

    visit(ast.parse(source), "")
    return result


def source_annotation(
    token: tokenize.TokenInfo,
    previous: tokenize.TokenInfo | None,
    lines: list[str],
) -> tuple[str, str] | None:
    """Require one diagnostic and its immediately preceding identified reason."""
    directive = re.match(
        r"#\s*(?:noqa\b|ruff:\s*noqa\b|type:\s*ignore\b|pyright:\s*ignore\b|pragma:\s*no (?:cover|branch)\b)",
        token.string,
        flags=re.IGNORECASE,
    )
    if directive is None:
        return None
    diagnostic = re.fullmatch(r"# noqa: (S603)", token.string)
    if diagnostic is None:
        raise PreferenceCheckError("unsupported_source_suppression")
    if previous is None:
        raise PreferenceCheckError("preceding_reason_required")
    reason = re.fullmatch(
        r"# policy-exception: ([A-Z][A-Z0-9-]+) -- \S.*", previous.string
    )
    if reason is None or lines[previous.start[0] - 1].strip() != previous.string:
        raise PreferenceCheckError("preceding_reason_required")
    return diagnostic.group(1), reason.group(1)


def source_exceptions(
    sources: dict[str, str],
) -> dict[str, tuple[str, str, tuple[str, ...]]]:
    """Inventory exact source suppressions and their actual enclosing symbols."""
    result: dict[str, tuple[str, str, tuple[str, ...]]] = {}
    for path, source in sources.items():
        symbols = definitions(source)
        comments = {
            token.start[0]: token
            for token in tokenize.generate_tokens(io.StringIO(source).readline)
            if token.type == tokenize.COMMENT
        }
        lines = source.split("\n")
        for line, token in comments.items():
            annotation = source_annotation(token, comments.get(line - 1), lines)
            if annotation is None:
                continue
            diagnostic, identifier = annotation
            candidates = [
                name
                for name, (start, end, kind) in symbols.items()
                if kind == "function" and start <= token.start[0] <= end
            ]
            if not candidates or identifier in result:
                raise PreferenceCheckError("ambiguous_source_suppression")
            symbol = max(candidates, key=lambda name: name.count("."))
            result[identifier] = (diagnostic, path, (symbol,))
    return result
