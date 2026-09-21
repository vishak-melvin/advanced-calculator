import math
OPERATORS = "-+*/()[]{}^,"

FUNCTIONS = {
    "log": (math.log, 1, 2)
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

    def current(self):
        if self.position >= len(tokens):
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

            if name not in FUNCTIONS:
                raise ValueError(f"Invalid Function: {name}")
            token.append(name)
        else:
            raise ValueError(f"Invalid character: {char}")
    return token

while(True):
    expression = input("enter an expression: ")
    if not expression.strip():
        raise ValueError("Expression cannot be empty")
    try:
        if(expression=="exit"):
            break
        tokens = tokenizer(expression)
        parser = Parser(tokens)
        result = parser.expression()
        print(result)
    except ValueError as error:
        print("Error:", error)
    except ZeroDivisionError:
        print("Error: division by zero")