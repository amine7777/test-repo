import math


def is_prime(n: int) -> bool:
    """Return True if n is a prime number, False otherwise.

    Uses trial division up to sqrt(n). Handles edge cases such as
    negative numbers, 0, and 1. Performance is O(sqrt(n)); suitable
    for typical use cases. For very large numbers consider a
    probabilistic primality test.
    """
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, math.isqrt(n) + 1, 2):
        if n % i == 0:
            return False
    return True


def _run_tests() -> None:
    test_cases = [
        (2, True),
        (17, True),
        (100, False),
        (1, False),
        (-5, False),
        (0, False),
        (3, True),
        (97, True),
        (49, False),
    ]
    all_passed = True
    for n, expected in test_cases:
        result = is_prime(n)
        status = "PASS" if result == expected else "FAIL"
        if status == "FAIL":
            all_passed = False
        print(f"{status}: is_prime({n}) == {result} (expected {expected})")
    if all_passed:
        print("\nAll tests passed.")
    else:
        print("\nSome tests FAILED.")
        raise SystemExit(1)


if __name__ == "__main__":
    _run_tests()
