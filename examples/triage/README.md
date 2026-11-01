# A minimal source-only triage

The target is [clamp.py](clamp.py). Its contract is: for an integer input,
return that integer when it is between 0 and 10 inclusive; return 0 below
that interval and 10 above it. Non-integer inputs are outside this example.

From the repository root, create a complete investigator packet:

```sh
python3 scripts/build_packet.py --role holmes --header examples/triage/header.json --out .runs/example-holmes.md
```

The command assembles the packet and refuses to overwrite it. It does not
start a model. In a host with the installed skill, use this request with the
source and contract available:

```text
Use Baker Street to check examples/triage/clamp.py against the integer contract
in examples/triage/README.md. Triage, plain voice, source inspection only.
Save the compact case outside the target. Do not edit or execute the target.
```

## Worked reasoning

For an integer `x < 0`, `min(10, x)` is `x`, and the outer `max` returns 0.
For `0 <= x <= 10`, the inner and outer operations both leave `x` unchanged.
For `x > 10`, the inner operation returns 10, which the outer operation retains.
Thus the source supports the entire stated integer contract, including 0 and 10.

A suitable scoped result is READY with no required repairs, based on SOURCE
and INFERENCE. It must disclose that no runtime test was performed, no
non-integer behavior was assessed, and the triage decision check was a
SEQUENTIAL_SELF_CHECK if performed by the same context. Watson, Moriarty, and
recall are not part of triage. This is a worked teaching example, not a recorded
agent evaluation or a required wording template.
