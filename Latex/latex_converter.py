FUNCTION = {
    "sin": r"\sin",
    "cos": r"\cos",
    "tan": r"\tan",
    "log": r"\log",
}

CONSTANT = {
    "pi": r"\pi",
    "e": "e",
    "tau": r"\tau",
    "phi": r"\varphi",
}

BRACKET = {
    "(": ("(",")"),
    "[": ("[","]"),
    "{": (r"\{",r"\}"),
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

        raise ValueError(f"unknown operator: {op}")

    if kind == "func":
        _, name, arguments = node
        if name == "log":
            if len(arguments) == 1:
                return rf"\ln\left({toLatex(arguments[0])}\right)"

            value = toLatex(arguments[0])
            base = toLatex(arguments[1])
            return rf"\log_{{{base}}}\left({value}\right)"

        function = FUNCTION.get(name, rf"\operatorname{{{name}}}")
        args = ",".join(toLatex(arg) for arg in arguments)
        return rf"{function}\left({args}\right)"

    if kind == "imul":
        return f"{toLatex(node[1])}{toLatex(node[2])}"

    raise ValueError(f"Unknown AST node: {kind}")
