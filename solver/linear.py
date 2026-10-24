def simple_linear(poly):
    a = 0
    b = 0
    for monomial, coeff in poly.items():
        if not monomial:
            b += coeff
        else:
            a += coeff
    if a == 0:
        if b == 0:
            return "infinite solutions"
        return "no solutions"
    x = -b/a
    return [x]
