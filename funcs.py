import math
def factorial(x):
    return math.gamma(x+1)

def clean_trig(func, x):
    result = func(x)
    if abs(result) < 1e-15 * max(1.0, abs(x)):
        return 0.0
    return result

def to_rad(val):
    if state["angle"] == "deg":
        val = math.radians(val)
    return val

def sin(val):
    return clean_trig(math.sin,to_rad(val))
def cos(val):
    return clean_trig(math.cos,to_rad(val))
def tan(val):
    return clean_trig(math.tan,to_rad(val))