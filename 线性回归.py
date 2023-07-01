import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

x = np.array([1, 2, 3])
y = np.array([1, 2, 4])

model = LinearRegression()
model.fit(x.reshape(-1, 1), y)

k, b = model.coef_, model.intercept_
print(k, b)

plt.scatter(x, y, c='r')
plt.plot(x, k[0] * x + b, c='g')
plt.show()