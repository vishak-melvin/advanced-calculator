def mode(state,*val):
    if len(val)==0:
        print(f"Formatting mode: {state["mode"]}")
        print(f"Angle mode: {state["angle"]}")
    else:
        if len(val) > 2:
            raise ValueError("mode cannot have more than 2 arguements")
        for value in val:
            if value in ("sci","dec"):
                state["mode"] = value
                print(f"switched formatting to {value} mode")
            elif value in ("rad","deg"):
                state["angle"] = value
                print(f"switched angle mode to {value}")
            else:
                raise ValueError(f"invalid mode: {value}")

def precision(state,*val):
    if len(val)==0:
        print(f"current precision is {state["precision"]}")
        return
    if len(val) > 1:
        raise ValueError("precision cannot have more than 1 arguement")
    
    try:
        val = int(val)
    except:
        raise ValueError("value must be an integer")
    if val < 0:
        raise ValueError("value must be non negetive")
    elif val > 50:
        raise ValueError("precision cannot be more than 50")
    state["precision"] = val


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