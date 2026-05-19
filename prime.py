def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n ** 0.5) + 1, 2):
        if n % i == 0:
            return False
    return True


if __name__ == "__main__":
    test_cases = [
        (-1, False),
        (0, False),
        (1, False),
        (2, True),
        (3, True),
        (4, False),
        (5, True),
        (9, False),
        (13, True),
        (97, True),
        (100, False),
    ]

    all_passed = True
    for number, expected in test_cases:
        result = is_prime(number)
        status = "PASS" if result == expected else "FAIL"
        if status == "FAIL":
            all_passed = False
        print(f"{status}: is_prime({number}) = {result} (expected {expected})")

    if all_passed:
        print("\nAll tests passed.")
    else:
        print("\nSome tests failed.")
