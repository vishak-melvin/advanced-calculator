from engine.state import state
from engine.help import help_text
from engine.variable import VARIABLE, save

def vars(state, *args):
    from engine.calculator import format
    if not VARIABLE:
        return "no variables stored"
    return "\n".join(
        f"{name} = {format(value, state.format, state.precision)}"
        for name, value in sorted(VARIABLE.items())
    )

def clear_vars(state, *names):
    if not names:
        VARIABLE.clear()
        save()
        return "Cleared all variables"
    for name in names:
        if name not in VARIABLE:
            raise ValueError(f"Undefined Variable: {name}")
    for name in names:
        del VARIABLE[name]
    save()
    return "Cleared "+", ".join(names)

def mode(state,*val):
    if len(val)==0:
        return(f"Formatting mode: {state.format} \nAngle mode: {state.angle}")
    
    if len(val) > 2:
        raise ValueError("mode cannot have more than 2 arguements")

    message = []
    for value in val:
        if value in ("sci","dec"):
            state.format = value
            message.append(f"switched formatting to {value} mode")
        elif value in ("rad","deg"):
            state.angle = value
            message.append(f"switched angle mode to {value}")
        else:
            raise ValueError(f"invalid mode: {value}")
    return "\n".join(message)

def precision(state,*val):
    if len(val)==0:
        return(f"current precision is {state.precision}")
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
    state.precision = val

def help(state, *val):
    return help_text("".join(val))

COMMANDS = {
    "mode":mode,
    "help":help,
    "precision": precision,
    "var": vars,
    "clear_var":clear_vars,
}