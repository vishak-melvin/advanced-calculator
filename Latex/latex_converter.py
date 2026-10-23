import re

from engine.calculator import parse, FUNC_ASSIGN, ASSIGNMENT

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
    "inf": r"\infty",
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

def name_latex(name):
    if len(name) == 1:
        return name
    else:
        return rf"\operatorname{{{name}}}"

def toLatex(expression):
    solve_match = re.fullmatch(r"\s*solve\s*\((.*)\)\s*", expression, re.DOTALL)
    if solve_match:
        return node_toLatex(parse(solve_match.group(1)))

    match = FUNC_ASSIGN.fullmatch(expression)
    if match:
        name, rparams, body = match.groups()
        params = ",".join(p.strip() for p in rparams.split(","))
        return rf"{name_latex(name)}\left({params}\right) = {node_toLatex(parse(body))}"

    match = ASSIGNMENT.fullmatch(expression)
    if match:
        name, expr = match.groups()
        return rf"{name} = {node_toLatex(parse(expr))}"

    return node_toLatex(parse(expression))

def node_toLatex(node):
    kind = node[0]
    if kind == "eq":
        return f"{node_toLatex(node[1])} = {node_toLatex(node[2])}"
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
        return rf"\left{left}{node_toLatex(inner)}\right{right}"

    if kind == "matrix":
        rows = node[1]
        latex_rows = [
            " & ".join(node_toLatex(element) for element in row)
            for row in rows
        ]

        return(
            r"\begin{bmatrix}"
            + r" \\ ".join(latex_rows)
            + r"\end{bmatrix}"
        )

    if kind == "neg":
        return rf"-{node_toLatex(node[1])}"

    if kind == "pow":
        _, base, exponent = node
        return rf"{node_toLatex(base)}^{{{node_toLatex(unwrap(exponent))}}}"

    if kind == "bin":
        _, op, left, right = node

        if op == "/":
            numerator = node_toLatex(unwrap(left))
            denominator = node_toLatex(unwrap(right))
            return rf"\frac{{{(numerator)}}}{{{denominator}}}"

        left = node_toLatex(left)
        right = node_toLatex(right)

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
        args = [node_toLatex(a) for a in arguments]

        if name in CUSTOM_FUNCS:
            return CUSTOM_FUNCS[name](*args)

        function = FUNCTION.get(name, rf"\operatorname{{{name}}}")
        return rf"{function}\left({','.join(args)}\right)"

    if kind == "imul":
        return f"{node_toLatex(node[1])} {node_toLatex(node[2])}"

    if kind == "post":
        _, op, operand = node
        return rf"{{{node_toLatex(operand)}{op}}}"

    if kind == "var":
        return node[1]

    if kind == "ufunc":
        _, name, arguments = node
        args = ",".join(node_toLatex(a) for a in arguments)
        return rf"{name_latex(name)}\left({args}\right)"

    raise ValueError(f"Unknown AST node: {kind}")
