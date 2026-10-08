import sys
from calculator import process, format, state
from commands import COMMANDS

from PySide6.QtWidgets import(QApplication, QMainWindow, QLineEdit,
QVBoxLayout, QWidget, QLabel)
app = QApplication(sys.argv)

window = QMainWindow()
window.setWindowTitle("Calculator")

central = QWidget()
layout = QVBoxLayout(central)
result_label = QLabel()

input_box = QLineEdit()
window.setCentralWidget(input_box)
layout.addWidget(result_label)
layout.addStretch()
layout.addWidget(input_box)
window.setCentralWidget(central)

def evaluate():
    expression = input_box.text()
    try:
        result = process(expression)
        if result is not None:
            result_label.setText(result)

    except ValueError as error:
        result_label.setText(("Error:", error))

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