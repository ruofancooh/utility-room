from typing import Any, Callable


def ti(fun: Callable) -> None:
    print(fun.__doc__)
    while True:
        print(fun(*(input().split())))


def ta(fun: Callable, args_set: set[Any]) -> None:
    print(fun.__doc__)
    for args in args_set:
        print(fun(*args))
