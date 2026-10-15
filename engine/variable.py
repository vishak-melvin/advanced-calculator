import json, os
from pathlib import Path

PATH = Path.home() / ".pycalc" / "variables.json"
VARIABLE = {}

def _encode(v):
    return {"re":v.real, "im":v.imag} if isinstance(v, complex) else v

def _decode(v):
    return complex(v["re"], v["im"]) if isinstance(v, dict) else v

def load():
    try:
        data = json.loads(PATH.read_text())
        loaded = {k:_decode(v) for k,v in data.items()}
    except Exception:
        return
    VARIABLE.clear()
    VARIABLE.update(loaded)

def save():
    try:
        PATH.parent.mkdir(parents=True, exist_ok=True)
        tmp = PATH.with_suffix(".tmp")
        tmp.write_text(json.dumps({k:_encode(v) for k,v in VARIABLE.items()}))
        os.replace(tmp, PATH)
    except OSError:
        pass