Review the release note against the complete function. The contract is limited to integer inputs. Decide whether this narrow change is ready. No runtime experiment is requested.

Claims to assess:
- C1: For integer inputs, clamp returns a value in [0, 10].
- C2: clamp(0) == 0 and clamp(10) == 10.
