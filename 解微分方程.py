import sympy as sy

x = sy.symbols("x")
a = sy.symbols("a")
b = sy.symbols("b")
f = sy.Function("f")
equation = (f(x).diff(x, 1) + a) * f(x) - b
result = sy.dsolve(equation, f(x))
sy.pprint(result)
