import math, cmath
from engine.state import state
def factorial(x):
    if x == int(x):          # integer-valued input, including 5.0
        x = int(x)
        if x < 0:
            raise ValueError("factorial is undefined for negative integers")
        return math.factorial(x)
    return math.gamma(x + 1)

def _TOInt(x):
    if isinstance(x, complex):
        if x.imag != 0:
            raise ValueError("expected a real integer")
        x = x.real
    r = round(x)
    if not math.isclose(x, r, rel_tol=0, abs_tol=1e-9):
        raise ValueError("expected a integer")
    return r

def _m(x):
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

def from_rad(val):
    if state.angle == "deg":
        val = val * 180/math.pi
    return val
# basic trig
def sin(val):
    x = to_rad(val)
    return clean_trig(_m(x).sin,x)
def cos(val):
    x = to_rad(val)
    return clean_trig(_m(x).cos,x)
def tan(val):
    if state.angle == "deg":
        if val % 180 == 90:
            return math.inf
        x = to_rad(val)
    else:
        x = val
        if abs(math.cos(x)) < 1e-15:
            return math.inf
    return clean_trig(_m(x).tan, x)

# hyperbolic trig
def sinh(x):
    return _m(x).sinh(x)
def cosh(x):
    return _m(x).cosh(x)
def tanh(x):
    return _m(x).tanh(x)

# inverse trig
def asin(x):
    result = _m(x).asin(x)
    return from_rad(result)
def acos(x):
    result = _m(x).acos(x)
    return from_rad(result) 
def atan(x):
    result = _m(x).atan(x)
    return from_rad(result) 

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
    return math.gcd(*(_TOInt(a) for a in args))

def lcm(*args):
    return math.lcm(*(_TOInt(a) for a in args))

def perm(n, r):
    return math.perm(_TOInt(n), _TOInt(r))

def comb(n, r):
    return math.comb(_TOInt(n), _TOInt(r))

def round_(val, dig=None):
    return round(val) if dig==None else round(val,_TOInt(dig))