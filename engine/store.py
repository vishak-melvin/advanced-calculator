import json, os
from pathlib import Path

MAIN = Path.home() / ".pycalc"
VARIABLE_PATH = MAIN / "variables.json"
FUNCTION_PATH = MAIN / "functions.json"
VARIABLE = {}
USER_FUNCTIONS = {}

def _read(path):
    try:
        return json.loads(path.read_text())
    except Exception:
        return {}

def _write(path, data):
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(".tmp")
        tmp.write_text(json.dumps(data))
        os.replace(tmp, path)
    except OSError:
        pass

def _encode(v):
    return {"re":v.real, "im":v.imag} if isinstance(v, complex) else v

def _decode(v):
    return complex(v["re"], v["im"]) if isinstance(v, dict) else v

def load():
    try:
        variables = {k: _decode(v) for k,v in _read(VARIABLE_PATH).items()}
    except Exception:
        variables = {}
    try:
        functions = {k: {"params": list(v["params"]),
                         "body": str(v["body"])} for k,v in _read(FUNCTION_PATH).items()}
    except Exception:
        functions = {}
    VARIABLE.clear()
    VARIABLE.update(variables)
    USER_FUNCTIONS.clear()
    USER_FUNCTIONS.update(functions)

def save_var():
    _write(VARIABLE_PATH, {k: _encode(v) for k,v in VARIABLE.items()})
def save_func():
    _write(FUNCTION_PATH, USER_FUNCTIONS)