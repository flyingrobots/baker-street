P1: Small unit assertion checks acceptance of 10 against the count contract. It fails on the off-by-one mutant and passes on the corrected candidate, with isolated inputs. It already uses the maintained unit runner.
P2: A costly fuzzer found a count boundary defect; the full corpus is large, but one standalone input reproduces it and can be reduced into a small unit assertion. Its oracle is the count contract.
P3: A cross-version v1-writer/v2-reader matrix protects the migration contract. Versions and seeds are pinned. The project maintains a scheduled compatibility suite with sufficient budget.
P4: A getter probe compared two calls sharing one counter; isolated runs matched. The original comparison is invalid and its accusation is withdrawn.
