import sys
from engine.calculator import process
from Latex.latex_renderer import LatexRenderer
from Latex.latex_converter import toLatex
from engine.help import add_commands, help_text
from engine.store import USER_FUNCTIONS

from PySide6.QtWidgets import(QApplication, QMainWindow, QLineEdit,
QVBoxLayout, QWidget, QLabel, QScrollArea)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFontDatabase
app = QApplication(sys.argv)

GUI_COMMANDS = {
    "dark": "toggle dark mode for Latex preview",
    "func [function name]": "displays the function definition in latex"
}
pairs = {
    "[" : "[]",
    "(" : "()",
    "{" : "{}",
}

add_commands(GUI_COMMANDS, "gui")

latex_dark = False
def toggle_theme():
    global latex_dark
    latex_dark = not latex_dark
    preview.set_darkmode(latex_dark)

class History(QLineEdit):
    MAX_HISTORY = 100
    def __init__(self):
        super().__init__()
        self.history = []
        self.index = 0
        self.draft = ""

    def addToHistory(self, text):
        if text and (not self.history or self.history[-1] != text):
            self.history.append(text)
            if len(self.history) > self.MAX_HISTORY:
                self.history.pop(0)
        self.index = len(self.history)

    def keyPressEvent(self, event):
        key = event.key()
        if event.text() in pairs:
            self.insert(pairs[event.text()])
            self.setCursorPosition(self.cursorPosition() - 1)
        elif key == Qt.Key_Up:
            if self.index == len(self.history):
                self.draft = self.text()
            if self.index > 0:
                self.index -= 1
                self.setText(self.history[self.index])
        elif key == Qt.Key_Down:
            if self.index < len(self.history):
                self.index += 1
                if self.index == len(self.history):
                    self.setText(self.draft)
                else:
                    self.setText(self.history[self.index])
        else:
            super().keyPressEvent(event)

last_latex = None
preview_override = None
def update_preview(input_box, preview):
    global last_latex, preview_override
    expression = input_box.text().strip()
    if expression:
        preview_override = None
        try:
            latex = toLatex(expression)
        except Exception:
            return
    elif preview_override is not None:
        latex = preview_override
    else:
        latex = ""

    if latex != last_latex:
        last_latex = latex
        preview.set_latex(latex)
    

window = QMainWindow()
window.setWindowTitle("Calculator")

central = QWidget()
layout = QVBoxLayout(central)
result_label = QLabel()
result_label.setFont(QFontDatabase.systemFont(QFontDatabase.SystemFont.FixedFont))
intro_label = QLabel("type 'help' if unsure")

preview = LatexRenderer()
preview.setFixedHeight(100)

scroll_area = QScrollArea()
scroll_area.setWidget(result_label)
scroll_area.setWidgetResizable(True)
result_label.setWordWrap(True)
result_label.setAlignment(Qt.AlignmentFlag.AlignTop)


input_box = History()

preview_timer = QTimer()
preview_timer.setSingleShot(True)
preview_timer.setInterval(100)
preview_timer.timeout.connect(lambda: update_preview(input_box, preview))

layout.addWidget(intro_label)
layout.addWidget(preview)
layout.addWidget(scroll_area, 1)
layout.addWidget(input_box)
window.setCentralWidget(central)

input_box.textChanged.connect(lambda:preview_timer.start())

def evaluate():
    global preview_override
    expression = input_box.text()
    input_box.addToHistory(expression)
    preview_override = None

    if expression == "exit":
        window.close()
        return
    if expression == "help":
        cmd, _, arg = expression.strip().partition(" ")
        if cmd.lower() == "help":
            result_label.setText(help_text(arg))
            input_box.clear()
            return
        input_box.clear()
        return
    if expression == "dark":
        toggle_theme()
        result_label.setText(f"Latex dark mode: {'on' if latex_dark else 'off'}")
        input_box.clear()
        return

    command, _, arguments = expression.strip().partition(" ")
    if command == "func" and arguments.strip():
        names = arguments.split()
        try:
            if len(names) != 1:
                raise ValueError("usage: func [function name]")
            name = names[0]
            if name not in USER_FUNCTIONS:
                raise ValueError(f"undefined function {name}")
            definition = USER_FUNCTIONS[name]
            params = ",".join(definition["params"])
            preview_override = toLatex(
                f"{name}({params}) = {definition['body']}"
            )
            result_label.setText(f"{name} definition")
            preview_timer.stop()
            input_box.clear()
            update_preview(input_box, preview)
        except ValueError as error:
            result_label.setText(f"Error: {error}")
            input_box.clear()
        return
    
    intro_label.hide()

    try:
        result = process(expression)
        if result is not None:
            result_label.setText(result)

    except ValueError as error:
        result_label.setText((f"Error: {error}"))

    except ZeroDivisionError:
        result_label.setText(("Error: division by zero"))

    except OverflowError:
        result_label.setText(("Error: result too large"))

    except Exception as e:
        result_label.setText((f"Error: {e}"))
    input_box.clear()
    

input_box.returnPressed.connect(evaluate)

window.show()

sys.exit(app.exec())
