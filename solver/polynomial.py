import cmath

def quadratic(poly):
    a = 0
    b  = 0
    c = 0
    for monomial, coeff in poly.items():
        if not monomial:
            c += coeff
        for _var,deg in monomial:
            if deg == 2:
                a += coeff
            elif deg == 1:
                b += coeff

    x1, x2 = (-b + (cmath.sqrt((b**2)-4*a*c)))/(2*a), (-b - (cmath.sqrt((b**2)-4*a*c)))/(2*a)
    return x1, x2