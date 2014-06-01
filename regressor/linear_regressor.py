from numpy import polynomial as P

x = np.linspace(-1,1,51) # x "data": [-1, -0.96, ..., 0.96, 1]

y = x**3 - x + np.random.randn(len(x)) # x^3 - x + N(0,1) "noise"

c, stats = P.polyfit(x,y,3,full=True)



