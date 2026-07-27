import pytest
from prime import is_prime


def test_prime_numbers():
    # Prime numbers
    assert is_prime(2) is True
    assert is_prime(3) is True
    assert is_prime(5) is True
    assert is_prime(7) is True
    assert is_prime(11) is True


def test_non_prime_numbers():
    # Non-prime numbers
    assert is_prime(4) is False
    assert is_prime(6) is False
    assert is_prime(8) is False
    assert is_prime(9) is False
    assert is_prime(10) is False


def test_edge_cases():
    # Edge cases
    assert is_prime(0) is False
    assert is_prime(1) is False
    assert is_prime(-1) is False
    assert is_prime(-5) is False
    assert is_prime(-12) is False


def test_large_prime():
    # Additional sanity check for a larger prime
    assert is_prime(13) is True
    assert is_prime(17) is True
    assert is_prime(19) is True


def test_large_non_prime():
    # Additional sanity check for a larger non-prime
    assert is_prime(15) is False
    assert is_prime(21) is False
    assert is_prime(25) is False