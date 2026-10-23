from engine.calculator import parse, CONSTANTS

def parse_eq(equation):
    if not equation.strip():
        raise ValueError("solve cannot be empty")
    #first create a list of valid equations
    systems = split_top_commas(equation)
    length = len(systems)
    if length > 1:
        raise ValueError("solve currently does not support system of equations")
    polynomials = []
    for eq in systems:
        if "=" not in eq:
            raise ValueError("equation must have = operator")
        # parse the equation to form an ast of format ("eq",lhs,rhs)
        ast = parse(eq)
        # analyze converts the eq ast into a polynomial rep. eg: {((var: degree),):coefficient}
        lhs = analyze(ast[1]) 
        rhs = analyze(ast[2])
        # equivelent to doing lhs-rhs = 0 where we ignore the =0 part
        polynomials.append(p_add(lhs,rhs,-1))
        
def split_top_commas(equations):
    depth = 0
    single_eq = []
    parts = []
    for char in equations:
        if char == "(": 
            depth += 1
            single_eq.append(char)
        elif char == ")":
            depth -= 1
            single_eq.append(char)
        elif depth == 0 and char == ",":
            parts.append("".join(single_eq).strip())
            single_eq = []
        else:
            single_eq.append(char)
    parts.append("".join(single_eq).strip())
    return parts

def p_const(c): return {(): c} if c != 0 else {}

def p_add(a, b, sign=1):
    out = dict(a)
    for m, c in b.items():
        out[m] = out.get(m, 0) + sign * c
        if out[m] == 0:
            del out[m]
    return out

def m_mul(m1, m2):
    powers = dict(m1)
    for v, p in m2:
        powers[v] = powers.get(v, 0) + p
    return tuple(sorted(powers.items()))

def p_mul(a, b):
    out = {}
    for m1, c1 in a.items():
        for m2, c2 in b.items():
            m = m_mul(m1, m2)
            out[m] = out.get(m, 0) + c1 * c2
    return {m: c for m, c in out.items() if c != 0}

def p_pow(a, n):
    result = {(): 1}
    for _ in range(n):
        result = p_mul(result, a)
    return result

def analyze(ast):
    kind = ast[0]
    if kind == "num":
        return p_const(float(ast[1]))
    if kind == "var":
        return {((ast[1], 1),): 1}
    if kind == "const":
        return p_const(CONSTANTS[ast[1]])
    if kind == "group":
        return analyze(ast[2])
    if kind == "neg":
        return {m: -c for m, c in analyze(ast[1]).items()}
    if kind == "bin":
        op = ast[1]
        left, right = analyze(ast[2]), analyze(ast[3])
        if op == "+": return p_add(left, right)
        if op == "-": return p_add(left, right, -1)
        if op == "*": return p_mul(left, right)
        if op == "/":
            if list(right) != [()]:
                raise ValueError("can only divide by a constant")
            d = right[()]
            return {m: c / d for m, c in left.items()}
    if kind == "pow":
        base, exp = analyze(ast[1]), analyze(ast[2])
        if not set(exp) <= {()}:
            raise ValueError("exponent must be a constant")
        n = exp.get((), 0)
        if n < 0 or n != int(n):
            raise ValueError("exponent must be a non-negative integer")
        return p_pow(base, int(n))
    if kind == "imul":
        return p_mul(analyze(ast[1]), analyze(ast[2]))
    raise ValueError(f"unsupported analyzer node: {kind}")