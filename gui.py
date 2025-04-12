import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QMessageBox
)
from anly_sint import parse_input  # Asegúrate de que retorna un string

class ConverterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Conversor Numérico")
        self.setGeometry(100, 100, 600, 500)

        self.layout = QVBoxLayout()

        self.input_label = QLabel("Número:")
        self.input_line = QLineEdit()
        self.input_line.setReadOnly(False)

        self.from_label = QLabel("Formato de origen:")
        self.from_combo = QComboBox()
        self.from_combo.addItems(["decimal", "binary", "ternary", "octal", "hexadecimal", "roman"])

        self.to_label = QLabel("Formato de destino:")
        self.to_combo = QComboBox()
        self.to_combo.addItems(["decimal", "binary", "ternary", "octal", "hexadecimal", "roman", "random"])

        self.convert_button = QPushButton("Convertir")
        self.convert_button.clicked.connect(self.convert)

        self.result_label = QLabel("Resultado:")
        self.result_output = QLabel("")
        self.result_output.setStyleSheet("font-weight: bold; color: green;")

        # Añadir widgets al layout
        self.layout.addWidget(self.input_label)
        self.layout.addWidget(self.input_line)
        self.layout.addWidget(self.from_label)
        self.layout.addWidget(self.from_combo)
        self.layout.addWidget(self.to_label)
        self.layout.addWidget(self.to_combo)
        self.layout.addWidget(self.convert_button)
        self.layout.addWidget(self.result_label)
        self.layout.addWidget(self.result_output)

        self.setLayout(self.layout)

    def convert(self):
        number = self.input_line.text()
        from_format = self.from_combo.currentText()
        to_format = self.to_combo.currentText()

        # Añadir prefijos si es necesario
        prefixed_number = self.add_prefix(number, from_format)

        command = f"{prefixed_number} to {to_format}"
        try:
            result = parse_input(command)
            self.result_output.setText(result)
            self.input_line.setReadOnly(False)
            self.input_line.setEnabled(True)
        except Exception as e:
            print(e)
            QMessageBox.critical(self, "Error", f"Ocurrió un error: {str(e)}")
            self.result_output.setText("")

    def add_prefix(self, number, fmt):
        if fmt == "binary" and not number.startswith("0b"):
            return "0b" + number
        elif fmt == "ternary" and not number.startswith("0t"):
            return "0t" + number
        elif fmt == "octal" and not number.startswith("0o"):
            return "0o" + number
        elif fmt == "hexadecimal" and not number.startswith("0x"):
            return "0x" + number
        else:
            return number

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ConverterApp()
    window.show()
    sys.exit(app.exec_())
