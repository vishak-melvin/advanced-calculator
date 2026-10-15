import math, cmath
from state import state
def factorial(x):
    return math.gamma(x+1)

def toInt(x):
    if isinstance(x, complex):
        if x.imag != 0:
            raise ValueError("expected a real integer")
        x = x.real
    r = round(x)
    if not math.isclose(x, r, rel_tol=0, abs_tol=1e-9):
        raise ValueError("expected a integer")
    return r

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

def sqrt(x):
    if isinstance(x, complex) or x < 0:
        r = cmath.sqrt(x)
        return r.real if r.imag == 0 else r
    return math.sqrt(x)

def root(val,deg=None):
    if deg is None or deg == 2:
        return sqrt(val)
    if deg == 0:
        raise ValueError("degree cannot be 0")

    if isinstance(val, complex) or isinstance(deg,complex):
        return val ** (1/deg)

    if val < 0:
        if float(deg).is_integer() and int(deg) % 2 == 1:
            r = -((-val)) ** (1/deg)
        else:
            r = val ** (1/deg)
            return r.real if r.imag == 0 else r
    else:
        return val ** (1/deg)

    n = round(r)
    if float(deg).is_integer() and n**int(deg) == val:
        return float(n)
    return r

def gcd(*args):
    return math.gcd(*(toInt(a) for a in args))

def lcm(*args):
    return math.lcm(*(toInt(a) for a in args))

def perm(n, r):
    return math.perm(toInt(n), toInt(r))

def comb(n, r):
    return math.comb(toInt(n), toInt(r))