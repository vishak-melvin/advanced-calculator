from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
import os

from help import add_commands
from calculator import process

TERMINAL_COMMANDS = {
    "clear": "-clears all previous text"
}
add_commands(TERMINAL_COMMANDS, "terminal")

def clear():
    os.system("cls" if os.name == "nt" else "clear")
    print("\033[3J", end="", flush=True)  

history = InMemoryHistory()
session = PromptSession(history=history)
print("you can enter 'help' if you're unsure")
while True:
    try:
        expression = session.prompt("enter an expression: ")
        if expression == "exit":
            break
        if expression == "clear":
            clear()
            continue

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