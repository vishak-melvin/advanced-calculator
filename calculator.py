import math
from commands import COMMANDS

state = {
    "mode": "dec",
    "precision": 9,
    "angle": "rad",
}

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

OPERATORS = "-+*/()[]{}^,"

FUNCTIONS = {
    "log": (math.log, 1, 2),
    "sin": (sin, 1, 1),
    "tan": (tan, 1, 1),
    "cos": (cos, 1, 1),
}

CONSTANTS = {
    "pi": math.pi,
    "e": math.e,
    "tau": math.tau,
    "phi": (1 + math.sqrt(5)) / 2,
}

closing_bracket = {
    "(": ")",
    "[": "]",
    "{": "}",
}

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def current(self):
        if self.position >= len(self.tokens):
            return None
        return self.tokens[self.position]

    def parse(self):
        node = self.expression()
        if self.current() is not None:
            raise ValueError(f"Unexpected token: {self.current()}")
        return node

    def expression(self):
        node = self.term()
        while self.current() in ("+", "-"):
            operator = self.current()
            self.position += 1
            right = self.term()
            node = ("bin", operator, node, right)
        return node

    def starts_factor(self):
        token = self.current()
        return token is not None and (token in closing_bracket or token in FUNCTIONS or token in CONSTANTS)

    def term(self):
        node = self.unary()
        while True:
            if self.current() in ("*", "/"):
                operator = self.current()
                self.position += 1
                right = self.unary()
                node = ("bin", operator, node, right)
            elif self.starts_factor():
                right = self.unary()
                node = ("imul", node, right)
            else:
                break
        return node

    def unary(self):
        if self.current() == "-":
            self.position += 1
            return ("neg", self.unary())
        elif self.current() == "+":
            self.position += 1
            return self.unary()
        return self.power()

    def power(self):
        base = self.factor()
        if self.current() == "^":
            self.position += 1
            exponent = self.unary()
            return ("pow", base, exponent)
        return base

    def factor(self):
        token = self.current()

        if token is None:
            raise ValueError("Expected a number or '('")

        if token in closing_bracket:
            closing = closing_bracket[token]
            self.position += 1
            inner = self.expression()
            if self.current() != closing:
                raise ValueError(f"Expected '{closing}'")
            self.position += 1
            return ("group", token, inner)

        if token in FUNCTIONS:
            return self.functions()

        if token in CONSTANTS:
            self.position += 1
            return ("const", token)

        if token in OPERATORS:
            raise ValueError(f"Unexpected token: {token}")

        self.position += 1
        return ("num", token)

    def functions(self):
        name = self.current()
        self.position += 1
        _, min_args, max_args = FUNCTIONS[name]

        if self.current() != "(":
            raise ValueError(f"Expected '(' after {name}")
        self.position += 1

        arguments = []
        if self.current() != ")":
            arguments.append(self.expression())
            while self.current() == ",":
                self.position += 1
                arguments.append(self.expression())

        if self.current() != ")":
            raise ValueError("Expected ')'")
        self.position += 1

        if not (min_args <= len(arguments) <= max_args):
            raise ValueError(f"{name} expects {min_args} to {max_args} arguments")
        return ("func", name, arguments)

def tokenizer(expression):
    token = []
    i = 0
    while i<len(expression):
        char = expression[i]
        if char.isdigit():
            digits = ""
            decimal_count = 0
            digit_count = 0

            while i<len(expression) and (expression[i].isdigit() or expression[i] == "."):
                if expression[i] == ".":
                    decimal_count += 1

                    if decimal_count > 1:
                        raise ValueError(f"Invalid number: {digits+expression[i]}")
                else:
                    digit_count += 1

                digits += expression[i]
                i += 1

            if i<len(expression) and expression[i] in "eE":
                digits += expression[i]
                i += 1
            
                if i<len(expression) and expression[i] in "-+":
                    digits += expression[i]
                    i += 1

                if i >= len(expression) or not expression[i].isdigit():
                    raise ValueError("invalid scientific notation")

                while i<len(expression) and expression[i].isdigit():
                    digits += expression[i]
                    i += 1

            if digit_count < 1:
                raise ValueError(f"invalid number: {digits}")
                
            token.append(digits)

        elif char in OPERATORS:
            token.append(char)
            i += 1
        
        elif char.isspace():
            i += 1

        elif char.isalpha():
            name = ""
            while i<len(expression) and (expression[i].isalpha()):
                name += expression[i]
                i += 1

            if name not in FUNCTIONS | CONSTANTS:
                raise ValueError(f"Invalid Function: {name}")
            token.append(name)
        else:
            raise ValueError(f"Invalid character: {char}")
    return token

def evaluate(node):
    kind = node[0]

    if kind == "num":
        return float(node[1])

    if kind == "const":
        return CONSTANTS[node[1]]

    if kind == "group":
        return evaluate(node[2])

    if kind == "neg":
        return -evaluate(node[1])

    if kind == "pow":
        return evaluate(node[1]) ** evaluate(node[2])

    if kind == "bin":
        _, op, left, right = node
        left, right = evaluate(left), evaluate(right)
        if op == "+": return left + right
        if op == "-": return left - right
        if op == "*": return left * right
        return left / right

    if kind == "func":
        _, name, args = node
        return FUNCTIONS[name][0](*[evaluate(a) for a in args])

    if kind == "imul":
        return evaluate(node[1]) * evaluate(node[2])

    raise ValueError(f"Unknown node: {kind}")

def parse(expression):
    return Parser(tokenizer(expression)).parse()

def calculate(expression):
    return evaluate(parse(expression))

def format(result, mode, precision):
    if mode == "dec":
        return f"{result:.{precision}g}"

    elif mode == "sci":
        return f"{result:.{precision}e}"

def process(expression):
    if not expression.strip():
        raise ValueError("Expression cannot be empty")

    parts = expression.split()
    command = parts[0]

    if command in COMMANDS:
        values = parts[1:]
        return COMMANDS[command](state, *values)

    result = calculate(expression)

    return format(
        result,
        state["mode"],
        state["precision"]
    )
