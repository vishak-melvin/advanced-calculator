from dataclasses import dataclass
import engine.functions as functions
import math,re

@dataclass
class Calcstate:
    angle: str = "rad"
    precision: int = 9
    format: str = "dec"

state = Calcstate()

OPERATORS = "-+*/()[]{}^,="
WORD_OPS = {"mod"}
ASSIGNMENT = re.compile(r"\s*([a-zA-Z])\s*=\s*(.+)\s*")
FUNC_ASSIGN = re.compile(r"""
    \s*
    ([a-zA-Z]+)
    \s* \( \s*
    ([a-zA-Z](?:\s*,\s*[a-zA-Z])*)
    \s* \) \s* = \s*
    (.+?)
    \s*
    """, re.VERBOSE)

FUNCTIONS = {
    "log": (functions.log, 1, 2),
    "sin": (functions.sin, 1, 1),
    "tan": (functions.tan, 1, 1),
    "cos": (functions.cos, 1, 1),
    "root": (functions.root, 1, 2),
    "abs": (abs, 1, 1),
    "floor": (math.floor, 1 , 1),
    "ceil": (math.ceil, 1, 1),
    "gcd": (functions.gcd , 1, None),
    "lcm": (functions.lcm, 1, None),
    "npr": (functions.perm, 2, 2),
    "ncr": (functions.comb, 2, 2),
    "sinh": (functions.sinh, 1, 1),
    "cosh": (functions.cosh, 1, 1),
    "tanh": (functions.tanh, 1, 1),
    "asin": (functions.asin, 1, 1),
    "acos": (functions.acos, 1, 1),
    "atan": (functions.atan, 1, 1),
    "round": (functions.round_, 1, 2),
    "det": (functions.determinant, 1, 1),
}

CONSTANTS = {
    "pi": math.pi,
    "e": math.e,
    "tau": math.tau,
    "phi": (1 + math.sqrt(5)) / 2,
    "i": complex(0,1),
    "inf": math.inf
}

closing_bracket = {
    "(": ")",
    "[": "]",
    "{": "}",
}

POSTFIX = {
    "!": (functions.factorial)
}