def sci(state):
    state["mode"] = "sci"
    print("switched to scientific notation")

def dec(state):
    state["mode"] = "dec"
    print("swicthed to decimal notation")


def mode(state):
    print(f"current mode is {state["mode"]}")

def precision(state,value=None):
    if value is None:
        print(f"current precision is {state["precision"]}")
    else:
        state["precision"] = value

def help(state):
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
exit        - Exit calculator
help        - Display this help
UP          - go up in history
DOWN        - go down in history
mode        - display current formatting mode
precision   - display decimal precision or set to value after command
        """
    )

COMMANDS = {
    "sci":sci,
    "dec":dec,
    "mode":mode,
    "help":help,
    "precision": precision
}