import sympy as sy

x = sy.symbols("x")
fx = sy.sin(x)
tl = fx.series(x, 0, 9)
sy.pprint(tl)
print(tl)