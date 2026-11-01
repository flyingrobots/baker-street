# Capacity accounting contract

The audience is a Python caller maintaining an in-memory reservation count.
All parameters must be plain integers: booleans and non-integers are rejected
with ValueError. Functions return an integer or raise ValueError, have no side
effects, and do not change caller state on rejection.

## reserve(used, count, capacity)

The valid starting state satisfies 0 <= used <= capacity. count must be positive.
A request succeeds exactly when used + count <= capacity, including an exact
fill. Its result is used + count. Requests beyond capacity raise ValueError.
Invalid starting state or count also raises ValueError.

## release(used, count)

used must be nonnegative. count must be positive and no greater than used.
A valid release returns used - count, including zero when all capacity is
released. Invalid counts raise ValueError.

## Scope

This API does not store data, synchronize callers, reserve external resources,
or provide thread safety. Those behaviors are outside this contract.
A reproducible violation requires a bounded repair; it is not by itself a
catastrophic or essential-use disqualifier. This contract is the acceptance bar.
