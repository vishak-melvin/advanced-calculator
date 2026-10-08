import math
from prompt_toolkit import prompt, PromptSession
from prompt_toolkit.history import InMemoryHistory
from commands import COMMANDS

def to_rad(val):
    if state["angle"] == "deg":
        val = math.radians(val)
    return val


def sin(val):
    return math.sin(to_rad(val))

def cos(val):
    return math.cos(to_rad(val))

def tan(val):
    return math.tan(to_rad(val))


OPERATORS = "-+*/()[]{}^,"

FUNCTIONS = {
    "log": (math.log, 1, 2),
    "sin": (sin,1,1),
    "tan": (tan,1,1),
    "cos": (cos,1,1),
}

CONSTANTS = {
    "pi": math.pi,
    "e": math.e,
    "tau": math.tau,
    "phi": (1+math.sqrt(5))/2,
}

closing_bracket = {
    "(": ")",
    "[": "]",
    "{": "}"
}
class Parser:
    def __init__(self,tokens):
        self.tokens = tokens
        self.position = 0

    def parse(self):
        value = self.expression()
        if self.current() is not None:
            raise ValueError(f"Unexpected token: {self.current()}")
        return value

    def current(self):
        if self.position >= len(self.tokens):
            return None
        return self.tokens[self.position]
    
    def factor(self):
        if self.current() in closing_bracket:
            opening = self.current()
            closing = closing_bracket[opening]
            self.position += 1
            value = self.expression()
            if self.position >= len(self.tokens) or self.current() != closing:
                raise ValueError(f"Expected '{closing}'")
            self.position += 1
            return value
        elif self.current() in FUNCTIONS:
            return self.functions()
        elif self.current() in CONSTANTS:
            value = CONSTANTS[self.current()]
            self.position += 1
            return value
        else:
            if self.current() is None:
                raise ValueError("Expected a number or '('")
            value = float(self.current())
            self.position += 1
            return value

    def functions(self):
        name = self.current()
        self.position += 1

        function, min_args, max_args = FUNCTIONS[name]

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

        if len(arguments) < min_args or len(arguments) > max_args:
            raise ValueError(f"{name} expects {min_args} to {max_args} arguements")
        return function(*arguments)
        


    def power(self):
        value = self.unary()
        if self.current() == "^":
            self.position += 1
            exponent = self.power()
            value = value ** exponent
        return value

    def unary(self):
        if self.current() == "-":
            self.position += 1
            value = self.unary()
            return -value
        elif self.current() == "+":
            self.position += 1
            value = self.unary()
            return value
        else:
            return self.factor();

    def term(self):
        value = self.power()

        while self.position < len(self.tokens) and self.current() in ("*","/"):
            operator = self.current()
            self.position += 1

            right = self.power()
            if operator == "*":
                value *= right
            else:
                value /= right
        return value

    def expression(self):
        value = self.term()

        while self.position < len(self.tokens) and self.current() in ("+","-"):
            operator = self.current()
            self.position += 1

            right = self.term()
            if operator == "+":
                value += right
            else:
                value -= right
        return value

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

def format(result,mode,precision):
    if mode == "dec":
        return f"{result:.{precision}f}"
    elif mode == "sci":
        return f"{result:.{precision}e}"

history = InMemoryHistory()
session = PromptSession(history=history)
print("you can enter 'help' if your unsure")
state = {
    "mode": "dec",
    "precision": 9,
    "angle": "rad",
}
while(True):
    expression = session.prompt("enter an expression: ")
    parts = expression.split()
    command = parts[0]
    if not expression.strip():
        raise ValueError("Expression cannot be empty")
    try:
        if command in COMMANDS:
            if len(parts)==1:
                COMMANDS[command](state)
            elif len(parts) > 1:
                value = parts[1:]
                COMMANDS[command](state,*value)
            continue
        if(expression=="exit"):
            break
        tokens = tokenizer(expression)
        parser = Parser(tokens)
        result = parser.parse()
        print(format(result,state["mode"],state["precision"]))
    except ValueError as error:
        print("Error:", error)
    except ZeroDivisionError:
        print("Error: division by zero")