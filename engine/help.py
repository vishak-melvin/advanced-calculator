# help.py
import difflib

# (name, category, summary, usage, details)
_ENTRIES = [
    # operators
    ("+",   "operators", "addition", "", ""),
    ("-",   "operators", "subtraction", "", ""),
    ("*",   "operators", "multiplication", "", ""),
    ("/",   "operators", "division", "", ""),
    ("^",   "operators", "exponentiation", "", ""),
    ("!",   "operators", "factorial", "", ""),
    ("mod", "operators", "modulus", "", ""),

    # functions
    ("log", "functions", "logarithm (natural by default)", "log(value, base)",
     "With one argument this is the natural log. The base is optional."),
    ("sin", "functions", "sine", "sin(x)", "Honors the current angle mode."),
    ("cos", "functions", "cosine", "cos(x)", "Honors the current angle mode."),
    ("tan", "functions", "tangent", "tan(x)", "Honors the current angle mode."),
    ("root", "functions", "nth root (square root by default)", "root(value[, degree])",
     "Odd roots of negative numbers return the real root."),
    ("npr", "functions", "permutations", "npr(n, r)", ""),
    ("ncr", "functions", "combinations", "ncr(n, r)", ""),
    ("abs", "functions", "absolute value", "abs(x)", ""),
    ("gcd", "functions", "greatest common divisor", "gcd(a, b, ...)", "Arguments must be integers."),
    ("lcm", "functions", "least common multiple", "lcm(a, b, ...)", "Arguments must be integers."),
    ("floor", "functions", "round down to an integer", "floor(x)", ""),
    ("ceil", "functions", "round up to an integer", "ceil(x)", ""),
    ("sinh", "functions", "hyperbolic sine", "sinh(x)", ""),
    ("cosh", "functions", "hyperbolic cosine", "cosh(x)", ""),
    ("tanh", "functions", "hyperbolic tangent", "tanh(x)", ""),
    ("asin", "functions", "inverse/arc sine", "asin(x)", "Honors the current angle mode."),
    ("acos", "functions", "inverse/arc cosine", "acos(x)", "Honors the current angle mode."),
    ("atan", "functions", "inverse/arc tangent", "atan(x)", "Honors the current angle mode."),
    ("round", "functions", "rounds value to nearest integer", "round(a,b)",
     "with one arguement, it rounds value to nearest integer. second arguement controls precision"),

    # constants
    ("pi",  "constants", "circle constant", "", ""),
    ("e",   "constants", "natural number", "", ""),
    ("tau", "constants", "2*pi", "", ""),
    ("phi", "constants", "golden ratio", "", ""),
    ("i", "constants", "imaginary unit", "", ""),
    ("inf", "constants", "infinity", "", ""),

    # modes
    ("sci", "modes", "scientific notation", "", ""),
    ("dec", "modes", "decimal notation", "", ""),
    ("rad", "modes", "use radians", "", ""),
    ("deg", "modes", "use degrees", "", ""),

    # commands
    ("exit", "commands", "exit the calculator", "", ""),
    ("help", "commands", "show help", "help [topic]", ""),
    ("mode", "commands", "show current formatting mode", "", ""),
    ("var", "commands", "display all stored variables and their values", "", ""),
    ("clear_var", "commands", "delete specified variables or all variable if not specified", "clear_var [variable name]", "if variable is not specified it WILL delete ALL variables"),
    ("func", "commands", "display all stored functions", "", ""),
    ("clear_func", "commands", "delete specified function or all functions if not specified", "clear_func [function name]", "if function is not specified it WILL delete ALL functions"),
]

SECTIONS = {
    "gui": "GUI-specific commands:",
    "terminal": "Terminal specific commands:"
}
CATEGORIES = ["operators", "functions", "constants", "modes", "commands"]

_INDEX = {e[0].lower(): e for e in _ENTRIES}


def add_commands(commands, section):
    for name, desc in commands.items():
        if name.lower() in _INDEX:
            continue
        entry = (name, section, desc, "", "")
        _ENTRIES.append(entry)
        _INDEX[name.lower()] = entry


def _unique(category):
    return sorted((e for e in _ENTRIES if e[1] == category), key=lambda e: e[0])


def _overview():
    lines = ["Type 'help <topic>' for details. Topics:", ""]
    for cat in CATEGORIES:
        names = [e[0] for e in _unique(cat)]
        preview = ", ".join(names[:6]) + (", ..." if len(names) > 6 else "")
        lines.append(f"  {cat:<10} {preview}")
    return "\n".join(lines)


def _category(cat):
    groups = [("", _unique(cat))]
    if cat == "commands":
        for key, title in SECTIONS.items():
            if _unique(key):
                groups.append((title, _unique(key)))

    width = max(len(e[0]) for _, entries in groups for e in entries)
    lines = []
    for title, entries in groups:
        if title:
            lines += ["", title]
        lines += [f"{e[0]:<{width}}  {e[2]}" for e in entries]
    return "\n".join(lines)


def _detail(e):
    name, _, summary, usage, details = e
    out = [f"{name}: {summary}"]
    if usage:
        out.append(f"  usage:  {usage}")
    if details:
        out.append(f"  {details}")
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