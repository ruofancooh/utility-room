from scipy.interpolate import lagrange
import numpy as np
from fractions import Fraction

x = np.array([1, 2, 3, 4, 5])
y = np.array([2, 4, 6, 114514, -1919810])
poly = lagrange(x, y)

lst = []
for i in poly.coef:
    lst.append(i)
print(lst)

for index, value in enumerate(lst):
    lst[index] = Fraction(value).limit_denominator()

print(lst)

#katex输出
katex = ''
for i in range(poly.order + 1):
    numerator = lst[i].numerator
    denominator = lst[i].denominator
    degree = poly.order - i
    if numerator > 0:
        sign = '+' if i != 0 else ''
    elif numerator < 0:
        sign = '-'
    else:
        continue

    if denominator != 1:
        coef = fr'{sign}\frac{{{abs(numerator)}}}{{{denominator}}}'
    else:
        coef = fr'{sign}{abs(numerator)}'

    if degree == 0:
        term = f'{coef}'
    elif degree == 1:
        term = f'{coef}x'
    else:
        term = f'{coef}x^{degree}'
    katex += term

row = f'f(x)&={katex}\\\\\n~\\\\\n'
for i in range(len(x)):
    row += f'f({x[i]})&={y[i]}\\\\\n'

katex = f'\\begin{{aligned}}\n{row}\\end{{aligned}}\n'
print(katex)

katex = f'$$\n{katex}$$\n'
with open('katex.md', 'w') as f:
    f.write(katex)