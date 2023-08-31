from typing import Callable


def t(fun: Callable) -> None:
    print(fun.__doc__)
    while True:
        print(fun(input()))
