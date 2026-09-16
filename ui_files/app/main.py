import sys
from PyQt6.QtWidgets import QApplication, QDialog, QMessageBox
from app.ui.primeros_pasos import Ui_Dialog

class MiDialogo(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.saludar)

    def saludar(self):
        QMessageBox.information(self, "Mensaje", "Has pulsado el botón")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = MiDialogo()
    ventana.setWindowTitle("Mi primera app PyQt6")
    ventana.resize(400, 300)
    ventana.show()
    sys.exit(app.exec())