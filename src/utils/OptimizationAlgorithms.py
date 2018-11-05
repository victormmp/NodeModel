"""
Support optimizaton methods.

Author: Victor Magalhães
Date: november 2018

"""

def golden_ratio(fun, eps=1e-3):
    """Golden ration unidimensional algorithm"""
    
    # Obtaining the best interval [a, b]
    
    s = 1e-2
    a = 1e-16
    b = s
    
    ta = fun(a)
    tb = fun(b)
    
    STEP = 2
    
    while(tb < ta):
        a = b
        ta = tb
        b *= 2
        tb = fun(b)
        STEP += 1
    
    if STEP <= 3:
        a = 1e-16
    else:
        a /= 2
    
    
    # Calculating the optimal solution
    
    xa = b - 0.618*(b - a)
    xb = a + 0.618*(b - a)
    
    ta = fun(xa)
    tb = fun(xb)
    
    while (b - a > eps):
        if ta > tb:
            a = xa
            xa = xb
            xb = a + 0.618*(b - a)
            ta = tb
            tb = fun(xb)
        else:
            b = xb
            xb = xa
            xa = b - 0.618*(b - a)
            tb = ta
            ta = fun(xa)
    
    optimal = (a + b) / 2
    
    return optimal
    
    
    
    