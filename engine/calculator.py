import math, re
from functools import lru_cache
from engine.commands import COMMANDS
from engine.state import state
from engine.matrix import Matrix
import engine.functions as functions
from engine.store import VARIABLE, load, USER_FUNCTIONS, save_func, save_var
load()
@lru_cache(maxsize=512)
def _parse_with(body, known):
    return parse(body)
def _parse_body(body):
    return _parse_with(body, tuple(sorted(USER_FUNCTIONS)))

OPERATORS = "-+*/()[]{}^,="
WORD_OPS = {"mod"}
ASSIGNMENT = re.compile(r"\s*([a-zA-Z])\s*=\s*(.+)\s*")
FUNC_ASSIGN = re.compile(r"""
    \s*
    ([a-zA-Z]+)
    \s* \( \s*
    ([a-zA-Z](?:\s*,\s*[a-zA-Z])*)
    \s* \) \s* = \s*
    (.+?)
    \s*
    """, re.VERBOSE)

def def_func(name, params, body):
    if name in FUNCTIONS or name in CONSTANTS or name in WORD_OPS or name in COMMANDS:
        raise ValueError(f"{name} is reserved")
    if name in VARIABLE:
        raise ValueError(f"{name} is already a variable")
    if len(set(params)) != len(params):
        raise ValueError("Duplicate parameter names")
    if any(p in CONSTANTS for p in params):
        raise ValueError("parameter cannot be a constant")
    if re.search(rf"\b{name}\b", body):
        raise ValueError("recursive defenition not supported")
    parse(body)
    USER_FUNCTIONS[name] = {"params": params, "body":body}
    save_func()

FUNCTIONS = {
    "log": (functions.log, 1, 2),
    "sin": (functions.sin, 1, 1),
    "tan": (functions.tan, 1, 1),
    "cos": (functions.cos, 1, 1),
    "root": (functions.root, 1, 2),
    "abs": (abs, 1, 1),
    "floor": (math.floor, 1 , 1),
    "ceil": (math.ceil, 1, 1),
    "gcd": (functions.gcd , 1, None),
    "lcm": (functions.lcm, 1, None),
    "npr": (functions.perm, 2, 2),
    "ncr": (functions.comb, 2, 2),
    "sinh": (functions.sinh, 1, 1),
    "cosh": (functions.cosh, 1, 1),
    "tanh": (functions.tanh, 1, 1),
    "asin": (functions.asin, 1, 1),
    "acos": (functions.acos, 1, 1),
    "atan": (functions.atan, 1, 1),
    "round": (functions.round_, 1, 2),
    "det": (functions.determinant, 1, 1),
}

CONSTANTS = {
    "pi": math.pi,
    "e": math.e,
    "tau": math.tau,
    "phi": (1 + math.sqrt(5)) / 2,
    "i": complex(0,1),
    "inf": math.inf
}

closing_bracket = {
    "(": ")",
    "[": "]",
    "{": "}",
}

POSTFIX = {
    "!": (functions.factorial)
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
        if self.current() == "=":
            self.position += 1
            right = self.expression()
            node = ("eq", node, right)
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
        return token is not None and (token in closing_bracket
                or token in FUNCTIONS or token in USER_FUNCTIONS or token in CONSTANTS or (token.isalpha() and len(token) == 1))

    def term(self):
        node = self.unary()
        while True:
            if self.current() in ("*", "/","mod"):
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

    def postfix(self):
        node = self.factor()
        while self.current() in ("!",):
            operator = self.current()
            self.position += 1
            node = ("post",operator,node)
        return node


    def power(self):
        base = self.postfix()
        if self.current() == "^":
            self.position += 1
            exponent = self.unary()
            return ("pow", base, exponent)
        return base

    def factor(self):
        token = self.current()

        if token is None:
            raise ValueError("Expected a number or '('")

        if token == "[":
            return self.matrix()

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

        if token in USER_FUNCTIONS:
            return self.user_function()

        if token in CONSTANTS:
            self.position += 1
            return ("const", token)

        if token.isalpha() and len(token) == 1:
            self.position += 1
            return("var", token)

        if token in OPERATORS or token in POSTFIX or token in WORD_OPS:
            raise ValueError(f"Unexpected token: {token}")

        self.position += 1
        return ("num", token)

    def matrix(self):
        if self.current() != "[":
            raise ValueError("expected [")
        self.position += 1
        rows = []
        while True:
            if self.current() != "[":
                raise ValueError("expected [ at beginning of row")
            self.position += 1
            row = []
            if self.current() == "]":
                raise ValueError("row cannot be empty")
            row.append(self.expression())
            while self.current() == ",":
                self.position += 1
                if self.current() in ("]", None):
                    raise ValueError("Expected matrix element")
                row.append(self.expression())
            if self.current() != "]":
                raise ValueError("expected row to close with ]")
            self.position += 1
            rows.append(row)

            if self.current() == ",":
                self.position += 1
                continue

            if self.current() != "]":
                raise ValueError("expected matrix to close with ]")
            self.position += 1
            break
        width = len(rows[0])
        if any(len(row) != width for row in rows):
            raise ValueError("all rows must be the same size as each other")
        return ("matrix", rows)

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

        if len(arguments) < min_args or (max_args is not None and len(arguments) > max_args):
            raise ValueError(f"{name} expects {min_args} to {max_args} arguments")
        return ("func", name, arguments)

    def user_function(self):
        name = self.current()
        self.position += 1
        return ("ufunc", name, self.arguments(name))

    def arguments(self, name):
        if self.current() != "(":
            raise ValueError("expected (")
        self.position += 1
        args = []
        if self.current() != ")":
            args.append(self.expression())
            while self.current() == ",":
                self.position += 1
                args.append(self.expression())
        if self.current() != ")":
            raise ValueError("expected )")
        self.position += 1
        return args

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

        elif char in OPERATORS or char in POSTFIX:
            token.append(char)
            i += 1
        
        elif char.isspace():
            i += 1

        elif char.isalpha():
            name = ""
            while i < len(expression) and expression[i].isalpha():
                name += expression[i]
                i += 1
            token.extend(split_name(name))
        else:
            raise ValueError(f"Invalid character: {char}")
    return token

valid = set(FUNCTIONS) | set(USER_FUNCTIONS) | WORD_OPS | set(CONSTANTS)
def split_name(name):
    pieces = []
    j = 0
    while j < len(name):
        for end in range(len(name), j, -1):      # longest match first
            if name[j:end] in valid:
                pieces.append(name[j:end])
                j = end
                break
        else:                                    # no known name starts here
            pieces.append(name[j])               # single-letter variable
            j += 1
    return pieces

def evaluate(node, env=None):
    kind = node[0]

    if kind == "num":
        return float(node[1])

    if kind == "const":
        return CONSTANTS[node[1]]

    if kind == "group":
        return evaluate(node[2], env)

    if kind == "matrix":
        rows = node[1]
        return Matrix([
            [evaluate(element, env) for element in row]
            for row in rows
        ])

    if kind == "neg":
        return -evaluate(node[1], env)

    if kind == "pow":
        return evaluate(node[1],env) ** evaluate(node[2],env)

    if kind == "bin":
        _, op, left, right = node
        left, right = evaluate(left,env), evaluate(right,env)
        if op == "+": return left + right
        if op == "-": return left - right
        if op == "*": return left * right
        if op == "/": return left / right
        if op == "mod": return left % right

    if kind == "func":
        _, name, args = node
        return FUNCTIONS[name][0](*[evaluate(a,env) for a in args])

    if kind == "imul":
        return evaluate(node[1],env) * evaluate(node[2],env)

    if kind == "post":
        _, op, operand = node
        return POSTFIX[op](*[evaluate(operand, env)])

    if kind == "var":
        name = node[1]
        if env and name in env:
            return env[name]
        if name in VARIABLE:
            return VARIABLE[name]
        raise ValueError(f"unidefined variable: {name}")

    if kind == "ufunc":
        _, name, args = node
        if name not in USER_FUNCTIONS:
            raise ValueError(f"undefined function: {name}")
        params = USER_FUNCTIONS[name]["params"]
        if len(args) != len(params):
            raise ValueError(f"{name} expects {len(params)} arguements")
        values = [evaluate(a, env) for a in args]
        body = _parse_body(USER_FUNCTIONS[name]["body"])
        return evaluate(body, dict(zip(params, values)))

    if kind == "eq":
        raise ValueError("equations must be used with solve()")

    raise ValueError(f"Unknown node: {kind}")

def parse(expression):
    return Parser(tokenizer(expression)).parse()

def calculate(expression):
    return evaluate(parse(expression))

def format(result, mode, precision):
    def format_num(value):
        if mode == "dec":
            formatted = f"{value:.{precision}g}"
        elif mode == "sci":
            formatted = f"{value:.{precision}e}"

        if formatted.startswith('-') and float(formatted) == 0:
            return formatted[1:]
        return formatted

    if isinstance(result, Matrix):
        return "[" + ", ".join(
            "[" + ", ".join(format(value, mode, precision) for value in row) + "]"
            for row in result.rows
        ) + "]"

    if isinstance(result, complex):
        real = result.real
        img = result.imag
        if img == 0:
            return format_num(real)
        if real == 0:
            if abs(img) == 1:
                return "-i" if img < 0 else "i"                
            else:
                return f"{"-" if img<0 else ''}{format_num(abs(img))}i"

        real_str = format_num(real)
        img_str = format_num(abs(img)) if abs(img) != 1 else ""

        sign = "-" if img<0 else "+"
        return f"{real_str}{sign}{img_str}i"
    return format_num(result)

def process(expression):
    if not expression.strip():
        raise ValueError("Expression cannot be empty")

    parts = expression.split()
    command = parts[0]
    if command in COMMANDS:
        values = parts[1:]
        return COMMANDS[command](state, *values)

    solve_match = re.fullmatch(r"\s*solve\s*\((.*)\)\s*", expression, re.DOTALL)
    if solve_match:
        return COMMANDS["solve"](state, solve_match.group(1))

    match = FUNC_ASSIGN.fullmatch(expression)
    if match:
        name, rparams, body = match.groups()
        params = [p.strip() for p in rparams.split(",")]
        def_func(name, params, body)
        return f"{name}({', '.join(params)}) = {body}"

    match = ASSIGNMENT.fullmatch(expression)
    if match:
        name, expr = match.groups()
        if name in CONSTANTS:
            raise ValueError(f"Cannot assign to constant {name}")
        if name in USER_FUNCTIONS:
            raise ValueError(f"{name} is already a user function")
        result = calculate(expr)
        VARIABLE[name] = result
        save_var()
    else:
        result = calculate(expression)

    return format(
        result,
        state.format,
        state.precision
    )
