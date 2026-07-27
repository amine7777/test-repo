def fib(n: int) -> int:
    """
    Return the nth Fibonacci number (0-indexed). Raises ValueError if n < 0.
    Args:
        n (int): Index of Fibonacci number (non-negative).
    Returns:
        int: Fibonacci number at position n.
    """
    if n < 0:
        raise ValueError("n must be a non-negative integer")
    if n == 0:
        return 0
    if n == 1:
        return 1
    
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b