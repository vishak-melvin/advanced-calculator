FUNCTION = {
    "sin": r"\sin",
    "cos": r"\cos",
    "tan": r"\tan",
    "gcd": r"\text{gcd}",
    "lcm": r"\text{lcm}",
    "sinh": r"\sinh",
    "cosh": r"\cosh",
    "tanh": r"\tanh",
    "asin": r"\arcsin",
    "acos": r"\arccos",
    "atan": r"\arctan",
}


def log(val, base=None):
    if base == None:
        return rf"\ln\left({{{val}}}\right)"
    return rf"\log_{{{base}}}\left({{{val}}}\right)"

def root(val, deg=None):
    if deg == None:
        return rf"\sqrt{{{val}}}"
    return rf"\sqrt[{deg}]{{{val}}}"

CUSTOM_FUNCS = {
    "log": log,
    "root": root,
    "npr": lambda n,r: rf"{{}}^{{{n}}}P_{{{r}}}",
    "ncr": lambda n,r: rf"\binom{{{n}}}{{{r}}}",
    "floor": lambda x: rf"\left\lfloor {x} \right\rfloor",
    "ceil": lambda x: rf"\left\lceil {x} \right\rceil",
    "abs": lambda x: rf"\left|{x}\right|",
}

CONSTANT = {
    "pi": r"\pi",
    "e": "e",
    "tau": r"\tau",
    "phi": r"\varphi",
    "i": "i",
}

BRACKET = {
    "(": ("(",")"),
    "[": ("[","]"),
    "{": (r"\{",r"\}"),
}

POSTFIX = {
    "!": "!"
}

def unwrap(node):
      return node[2] if node [0] == "group" else node

def toLatex(node):
    kind = node[0]
    if kind == "num":
        text = node[1].lower()
        if "e" in text:
            mantissa, exponent = text.split("e")
            return rf"{mantissa}\times 10^{{{int(exponent)}}}"
        return text

    if kind == "const":
        return CONSTANT[node[1]]

    if kind == "group":
        _, opening, inner = node
        left, right = BRACKET[opening]
        return rf"\left{left}{toLatex(inner)}\right{right}"

    if kind == "neg":
        return rf"-{toLatex(node[1])}"

    if kind == "pow":
        _, base, exponent = node
        return rf"{toLatex(base)}^{{{toLatex(unwrap(exponent))}}}"

    if kind == "bin":
        _, op, left, right = node

        if op == "/":
            numerator = toLatex(unwrap(left))
            denominator = toLatex(unwrap(right))
            return rf"\frac{{{(numerator)}}}{{{denominator}}}"

        left = toLatex(left)
        right = toLatex(right)

        if op == "+":
            return f"{left} + {right}"

        if op == "-":
            return f"{left} - {right}"

        if op == "*":
            return rf"{left} \cdot {right}"

        if op == "mod":
            return rf"{left} \bmod {right}"

        raise ValueError(f"unknown operator: {op}")

    if kind == "func":
        _, name, arguments = node
        args = [toLatex(a) for a in arguments]

        if name in CUSTOM_FUNCS:
            return CUSTOM_FUNCS[name](*args)

        function = FUNCTION.get(name, rf"\operatorname{{{name}}}")
        return rf"{function}\left({','.join(args)}\right)"

    if kind == "imul":
        return f"{toLatex(node[1])}{toLatex(node[2])}"

    if kind == "post":
        _, op, operand = node
        return rf"{{{toLatex(operand)}{op}}}"

    raise ValueError(f"Unknown AST node: {kind}")
