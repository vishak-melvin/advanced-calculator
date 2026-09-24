import math
from prompt_toolkit import prompt, PromptSession
from prompt_toolkit.history import InMemoryHistory


def help():
    print(
        """
OPERATORS:
+    - Addition
-    - Subraction
*    - Multiplication
/    - Division
^    - Exponentiation

FUNCTIONS:
log   - Logarithm

CONSTANTS:
pi     - circle constant
e      - natural number 
tau    - 2*pi
phi    - golden ratio

MODES:
sci - prefer scientific notation
dec - prefer decimal notation

COMMANDS:
exit  - Exit calculator
help  - Display this help
UP    - go up in history
DOWN  - go down in history
        """
    )

OPERATORS = "-+*/()[]{}^,"

FUNCTIONS = {
    "log": (math.log, 1, 2)
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

def format(result,mode):
    if mode == "dec":
        return str(result)
    elif mode == "sci":
        return f"{result:.3e}"

history = InMemoryHistory()
session = PromptSession(history=history)
print("you can enter 'help' if your unsure")
mode = "dec"
while(True):
    expression = session.prompt("enter an expression: ")
    if not expression.strip():
        raise ValueError("Expression cannot be empty")
    try:
        if(expression=="sci"):
            print("switched to scienctific notation")
            mode = "sci"
            continue
        elif(expression=="dec"):
            print("switched to decimal notation")
            mode = "dec"
            continue
        elif(expression=="mode"):
            print(f"current mode is {mode}")
            continue
        if(expression=="exit"):
            break
        if(expression=="help"):
            help()
            continue
        tokens = tokenizer(expression)
        parser = Parser(tokens)
        result = parser.parse()
        print(format(result,mode))
    except ValueError as error:
        print("Error:", error)
    except ZeroDivisionError:
        print("Error: division by zero")