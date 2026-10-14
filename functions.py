import math, cmath
from state import state
def factorial(x):
    return math.gamma(x+1)

def m(x):
    return cmath if isinstance(x, complex) else math 

def snap(r,x):
    return 0.0 if abs(r) < 1e-15 * max(1.0, abs(x)) else r

def clean_trig(func, x):
    result = func(x)
    if isinstance(result, complex):
        re, im= snap(result.real, x), snap(result.imag, x)
        return re if im == 0 else complex(re, im)
    return snap(result, x)

def to_rad(val):
    if state.angle == "deg":
        val = val * math.pi/180
    return val

def sin(val):
    x = to_rad(val)
    return clean_trig(m(x).sin,x)
def cos(val):
    x = to_rad(val)
    return clean_trig(m(x).cos,x)
def tan(val):
    x = to_rad(val)
    return clean_trig(m(x).tan,x)

def log(val, base = None):
    if isinstance(val, complex) or val<0:
        r = cmath.log(val) if base == None else cmath.log(val, base)
        return r.real if r.imag == 0 else r
    return math.log(val) if base == None else math.log(val, base)