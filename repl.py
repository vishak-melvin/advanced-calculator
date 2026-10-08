from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory

from calculator import process

history = InMemoryHistory()
session = PromptSession(history=history)
print("you can enter 'help' if you're unsure")
while True:
    try:
        expression = session.prompt("enter an expression: ")
        if expression == "exit":
            break

        result = process(expression)
        if result is not None:
            print(result)

    except ValueError as error:
        print("Error:", error)

    except ZeroDivisionError:
        print("Error: division by zero")

    except OverflowError:
        print("Error: result too large")

    except Exception as e:
        print(f"Error: {e}")