def mode(state,val=None):
    if val is None:
        print(f"Formatting mode: {state["mode"]}")
        print(f"Angle mode: {state["angle"]}")
    else:
        if val not in ("sci","dec","rad","deg"):
            raise ValueError("invalid mode")
        if val in ("sci","dec"):
            state["mode"] = val
            print(f"switched formatting to {val} mode")
        elif val in ("rad","deg"):
            state["angle"] = val
            print(f"switched angle mode to {val}")

def precision(state,value=None):
    if value is None:
        print(f"current precision is {state["precision"]}")
    else:
        try:
            value = int(value)
        except:
            raise ValueError("value must be an integer")
        if value < 0:
            raise ValueError("value must be non negetive")
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
precision   - display decimal precision or set a value after command
        """
    )

COMMANDS = {
    "mode":mode,
    "help":help,
    "precision": precision,
}