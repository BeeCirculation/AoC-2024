def cache(func):
    cache = {}
    def wrapper(*args):
        if args in cache:
            return cache[args]
        else:
            cache[args] = func(*args)
            return cache[args]
    return wrapper


def fib(n):
    if n == 1 or n == 2:
        return 1

    return fib(n-1) + fib(n-2)



