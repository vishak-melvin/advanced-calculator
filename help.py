# help.py
import difflib

_ENTRIES = [
    # operators
    ("+",   "operators", "addition", "", "", [], []),
    ("-",   "operators", "subtraction", "", "", [], []),
    ("*",   "operators", "multiplication", "", "", [], []),
    ("/",   "operators", "division", "", "", [], []),
    ("^",   "operators", "exponentiation", "", "", [("2^10", "1024")], []),
    ("!",   "operators", "factorial", "", "", [("5!", "120")], []),
    ("mod", "operators", "modulus", "", "", [("7 mod 3", "1")], []),

    # functions
    ("log", "functions", "logarithm (natural by default)", "log(value[, base])",
     "With one argument this is the natural log. The base is optional.",
     [("log(e)", "1"), ("log(8, 2)", "3")], ["ln"]),
    ("sin", "functions", "sine", "sin(x)", "Honors the current angle mode.",
     [("sin(90)", "1  (in deg mode)")], []),
    ("cos", "functions", "cosine", "cos(x)", "Honors the current angle mode.", [], []),
    ("tan", "functions", "tangent", "tan(x)", "Honors the current angle mode.", [], []),
    ("root", "functions", "nth root (square root by default)", "root(value[, degree])",
     "Odd roots of negative numbers return the real root.",
     [("root(27, 3)", "3")], []),
    ("nPr", "functions", "permutations", "nPr(n, r)", "", [("nPr(4, 3)", "24")], ["perm"]),
    ("nCr", "functions", "combinations", "nCr(n, r)", "", [("nCr(5, 2)", "10")], ["comb"]),

    # constants
    ("pi",  "constants", "circle constant", "", "", [], []),
    ("e",   "constants", "natural number", "", "", [], []),
    ("tau", "constants", "2*pi", "", "", [], []),
    ("phi", "constants", "golden ratio", "", "", [], []),
    ("i",   "constants", "imaginary unit", "", "", [], []),

    # modes
    ("sci", "modes", "scientific notation", "", "", [], []),
    ("dec", "modes", "decimal notation", "", "", [], []),
    ("rad", "modes", "use radians", "", "", [], []),
    ("deg", "modes", "use degrees", "", "", [], []),

    # commands
    ("exit", "commands", "exit the calculator", "", "", [], []),
    ("help", "commands", "show help", "help [topic]", "", [], []),
    ("mode", "commands", "show current formatting mode", "", "", [], []),
    ("precision", "commands", "show or set decimal precision", "precision [digits]", "", [], []),
]

CATEGORIES = ["operators", "functions", "constants", "modes", "commands"]

# name/alias (lowercase) -> entry tuple
_INDEX = {}
for _e in _ENTRIES:
    _INDEX[_e[0].lower()] = _e
    for _alias in _e[6]:
        _INDEX[_alias.lower()] = _e

# registers extra commands like gui specific commands
def add_commands(commands):
    for name, desc in commands.items():
        if name.lower() in _INDEX:
            continue
        entry = (name, "commands", desc, "", "", [], [])
        _ENTRIES.append(entry)
        _INDEX[name.lower()] = entry

def _unique(category):
    return sorted({e[0]: e for e in _ENTRIES if e[1] == category}.values(),
                  key=lambda e: e[0])


def _overview():
    lines = ["Type 'help <topic>' for details. Topics:", ""]
    for cat in CATEGORIES:
        names = [e[0] for e in _unique(cat)]
        preview = ", ".join(names[:6]) + (", ..." if len(names) > 6 else "")
        lines.append(f"  {cat:<10} {preview}")
    return "\n".join(lines)


def _category(cat):
    entries = _unique(cat)
    width = max(len(e[0]) for e in entries)
    return "\n".join(f"{e[0]:<{width}}  {e[2]}" for e in entries)


def _detail(e):
    name, _, summary, usage, details, examples, aliases = e
    out = [f"{name}: {summary}"]
    if usage:
        out.append(f"  usage:  {usage}")
    if details:
        out.append(f"  {details}")
    if aliases:
        out.append(f"  also:   {', '.join(aliases)}")
    for expr, result in examples:
        out.append(f"  {expr} = {result}")
    return "\n".join(out)


def help_text(query=""):
    query = query.strip().lower()
    if not query:
        return _overview()
    if query in CATEGORIES:
        return _category(query)
    if query in _INDEX:
        return _detail(_INDEX[query])
    close = difflib.get_close_matches(query, _INDEX, n=3)
    hint = f" Did you mean: {', '.join(close)}?" if close else ""
    return f"No help for '{query}'.{hint}"