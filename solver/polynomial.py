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

def n_degree(poly, max_deg, tol=1e-10):
    if max_deg > 500:
        raise ValueError("solver doesnt support solving all roots above degree 500")
    from solver.numerical import durand_kerner, clean
    coefficients = [0] * (max_deg+1)
    for monomial, coeff in poly.items():
        degree = monomial[0][1] if monomial else 0
        coefficients[max_deg-degree] += coeff
    result = durand_kerner(coefficients)
    clean_result = [clean(x) for x in result]
    return clean_result