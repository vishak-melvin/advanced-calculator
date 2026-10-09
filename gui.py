import sys
from calculator import process
from Latex.latex_renderer import LatexRenderer

from PySide6.QtWidgets import(QApplication, QMainWindow, QLineEdit,
QVBoxLayout, QWidget, QLabel, QScrollArea)
from PySide6.QtCore import Qt, QTimer
app = QApplication(sys.argv)

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
        if key == Qt.Key_Up:
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

def update_preview():
    expression = input_box.text()
    preview.set_latex(expression)
    

window = QMainWindow()
window.setWindowTitle("Calculator")

central = QWidget()
layout = QVBoxLayout(central)
result_label = QLabel()
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

layout.addWidget(intro_label)
layout.addWidget(preview)
layout.addWidget(scroll_area, 1)
layout.addWidget(input_box)
window.setCentralWidget(central)

input_box.textChanged.connect(lambda:preview_timer.start())
preview_timer.timeout.connect(update_preview)

def evaluate():
    expression = input_box.text()
    input_box.addToHistory(expression)

    if expression == "exit":
        window.close()
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