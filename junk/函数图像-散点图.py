import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False  #用来正常显示负号 #有中文出现的情况，需要u'内容'
fig = plt.figure(figsize=(5, 5))
ax = fig.add_subplot(111)

test = 2
if test == 1:
    x = np.linspace(-3, 3, 100)
    y = np.sin(x)
    plt.plot(x, y)
    plt.show()
elif test == 2:
    x = np.linspace(-3, 3, 300, dtype=complex)
    y = np.power(-1, x)
    #print(y)

    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.spines['bottom'].set_position(('data', 0))
    ax.yaxis.set_ticks_position('left')
    ax.spines['left'].set_position(('data', 0))

    plt.xlim((-3, 3))
    plt.ylim((-3, 3))

    plt.plot(x, y.real, c='r', label='实部')
    plt.plot(x, y.imag, c='g', label='虚部')

    plt.title(r'$y=(-1)^x$的实部和虚部')
    plt.legend()
    plt.show()
elif test == 3:
    plt.scatter([1, 2], [3, 4], c='r')
    plt.scatter([5, 6], [7, 8], c='g')
    plt.show()