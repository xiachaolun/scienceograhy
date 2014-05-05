import math

def f(n):
    return n * math.pow((n-1) / n, n * math.log(n) * math.log(n))

for n in xrange(2, 1000):
    print f(n * 1.0)