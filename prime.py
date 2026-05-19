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
    assert is_prime(-1) == False
    assert is_prime(0) == False
    assert is_prime(1) == False
    assert is_prime(2) == True
    assert is_prime(3) == True
    assert is_prime(4) == False
    assert is_prime(5) == True
    assert is_prime(9) == False
    assert is_prime(11) == True
    assert is_prime(13) == True
    assert is_prime(15) == False
    assert is_prime(17) == True
    assert is_prime(19) == True
    assert is_prime(25) == False
    assert is_prime(97) == True
    assert is_prime(100) == False
    print("All tests passed.")
