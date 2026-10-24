# this is where mathematical algorithms like root finders should live
import cmath, math, random
# polynomial solver that finds ALL roots
def durand_kerner(coeff, tol=1e-12, max_itr=1000):
    max_deg = len(coeff) - 1
    # normalize so that coeff represents a monic
    monic = coeff.copy()
    if monic[0] != 1:
        norm = monic[0]
        for i in range(len(monic)):
            monic[i] = monic[i]/norm

    R = 1 + max(abs(c) for c in monic[1:])
    z = [
        R * cmath.exp(1j * (2 * math.pi * i / max_deg + 0.4))
        for i in range(max_deg)
    ]

    converged = False
    for itr in range(max_itr):
        z_new = [0j] * max_deg
        delta_prev = float('inf')
        for i in range(max_deg):
            numerator = horner(z[i], monic)
            denominator = 1
            for j in range(max_deg):
                if j!=i:
                    denominator *= z[i] - z[j]
            if abs(denominator) < 1e-300:
                z_new[i] = z[i] + (random.uniform(-1,1) + 1j*random.uniform(-1,1)) * 1e-6
                continue
            z_new[i] = z[i] - (numerator/denominator)
        delta = max(abs(z_new[i]-z[i]) for i in range(max_deg))
        z = z_new
        if delta < tol:
            converged = True
            break
        if delta > 0.99*delta_prev:
            break
        delta_prev = delta

    max_residual = max(abs(horner(z[i],monic)) for i in range(max_deg))
    if not converged:
        if max_residual > 1e-8:
            raise ValueError("could not find accurate roots.")

    return z
    

# evaluates a poly eq given a value for x
def horner(x, coeff):
    result = 0
    for c in coeff:
        result = result * x + c
    return result

def clean(x, tol=1e-9):
    scale = max(1,abs(x))
    re = 0.0 if abs(x.real) < tol*scale else x.real
    im = 0.0 if abs(x.imag) < tol*scale else x.imag
    return re if im == 0 else complex(re, im)

