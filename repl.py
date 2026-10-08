from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory

from calculator import calculate, format, state
from commands import COMMANDS

history = InMemoryHistory()
session = PromptSession(history=history)
print("you can enter 'help' if you're unsure")
while True:
    try:
        expression = session.prompt("enter an expression: ")

        if not expression.strip():
            raise ValueError("Expression cannot be empty")

        if expression == "exit":
            break

        parts = expression.split()
        command = parts[0]

        if command in COMMANDS:
            values = parts[1:]
            COMMANDS[command](state, *values)
            continue

        result = calculate(expression)

        print(format(result, state["mode"], state["precision"]))

    except ValueError as error:
        print("Error:", error)

    except ZeroDivisionError:
        print("Error: division by zero")

    except OverflowError:
        print("Error: result too large")

    except Exception as e:
        print(f"Error: {e}")