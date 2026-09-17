class parser:
    def __init__(self,tokens):
        self.tokens = tokens
        self.position = 0

    def current(self):
        if self.position >= len(tokens):
            return None
        return self.tokens[self.position]
    
    def factor(self):
        if self.current() == "(":
            self.position += 1
            value = self.expression()
            if self.position >= len(tokens) or self.current() != ")":
                raise ValueError("Expected ')'")
            self.position += 1
            return value
        else:
            value = float(self.current())
            self.position += 1
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
        value = self.unary()

        while self.position < len(self.tokens) and self.current() in ("*","/"):
            operator = self.current()
            self.position += 1

            right = self.unary()
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

        elif char in "+-*/()":
            token.append(char)
            i += 1
        elif char.isspace():
            i += 1
        else:
            raise ValueError(f"Invalid character: {char}")
    return token

expression = input("enter an expression: ")
if not expression.strip():
    raise ValueError(f"Expression cannot be empty")

tokens = tokenizer(expression)
parser = parser(tokens)
result = parser.expression()
print(result)