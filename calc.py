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

def parser(tokens):
    position = 0

    def factor():
        nonlocal position

        if tokens[position] == "(":
            position += 1
            value = expression()
            if position >= len(tokens) or tokens[position] != ")":
                raise ValueError("Expected ')")
            position += 1
            return value
        else:
            value = float(tokens[position])
            position += 1
            return value

    def term():
        nonlocal position
        value = factor()

        while position < len(tokens) and tokens[position] in ("*","/"):
            operator = tokens[position]
            position += 1

            right = factor()
            if operator == "*":
                value *= right
            else:
                value /= right
        return value

    def expression():
        nonlocal position
        value = term()

        while position < len(tokens) and tokens[position] in ("+","-"):
            operator = tokens[position]
            position += 1

            right = term()
            if operator == "+":
                value += right
            else:
                value -= right
        return value

    result = expression()
    if position != len(tokens):
        raise ValueError(f"Unexpected token: {tokens[position]}")
    return result

expression = input("enter an expression: ")
if not expression.strip():
    raise ValueError(f"Expression cannot be empty")

tokens = tokenizer(expression)
result = parser(tokens)
print(result)