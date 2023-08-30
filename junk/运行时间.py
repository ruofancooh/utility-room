import time

start = end = time.perf_counter
N = 10**7

T1 = start()

for i in range(N):
    if i == N:
        pass
    else:
        pass

T2 = end()

T3 = start()

for i in range(N):
    if i != N:
        pass
    else:
        pass

T4 = end()

print('程序运行时间:%s毫秒' % ((T2 - T1) * 1000))
print('程序运行时间:%s毫秒' % ((T4 - T3) * 1000))
