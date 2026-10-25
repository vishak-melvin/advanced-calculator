# this is where mathematical algorithms like root finders should live
import cmath, math, random, sys
# polynomial solver that finds ALL roots
def durand_kerner(coeff, c_tol=10, max_itr=1000):
    max_deg = len(coeff) - 1
    # normalize so that coeff represents a monic
    monic = coeff.copy()
    if monic[0] != 1:
        norm = monic[0]
        for i in range(len(monic)):
            monic[i] = monic[i]/norm

    R = abs(monic[-1]) ** (1.0/max_deg) if monic[-1] != 0 else 1.0
    z = [
        R * cmath.exp(1j * (2 * math.pi * i / max_deg + 0.4))
        for i in range(max_deg)
    ]

    converged = [False] * max_deg
    EPS = sys.float_info.epsilon
    for itr in range(max_itr):
        for i in range(max_deg):
            if converged[i]:
                continue
            p, b = horner(z[i], monic)
            if abs(p) <= c_tol * EPS * b:
                converged[i] = True
                continue
            denominator = 1
            for j in range(max_deg):
                if j != i:
                    denominator *= z[i] - z[j]
            if abs(denominator) < 1e-300:
                z[i] += (random.uniform(-1,1) + 1j*random.uniform(-1,1))*1e-6
                continue
            z[i] -= p/denominator
        if all(converged):
            break
    else:
        worst = max(abs(p)/b for p,b in (horner(zi,monic) for zi in z))
        if worst >1e-8:
            raise ValueError("could not find accurate roots")

    return z
    

# evaluates a poly eq given a value for x. also returns bound as scale of error
def horner(x, coeff):
    p = coeff[0]
    b = abs(coeff[0])
    ax = abs(x)
    for c in coeff[1:]:
        p = p*x + c
        b = b*ax + abs(c)
    return p,b

# cleans roots based on relative tolerance
def clean(x, tol=1e-9):
    scale = max(1,abs(x))
    re = 0.0 if abs(x.real) < tol*scale else x.real
    im = 0.0 if abs(x.imag) < tol*scale else x.imag
    return re if im == 0 else complex(re, im)

