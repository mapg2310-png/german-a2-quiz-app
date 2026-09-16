from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QMessageBox

app = QApplication([])

ventana = QWidget()
ventana.setWindowTitle("Mi primera ventana PyQt6")

etiqueta = QLabel("Hola, esto es PyQt6 en Windows")
boton = QPushButton("Púlsame")

def al_pulsar():
    QMessageBox.information(ventana, "Mensaje", "Has pulsado el botón")

boton.clicked.connect(al_pulsar)

layout = QVBoxLayout()
layout.addWidget(etiqueta)
layout.addWidget(boton)

ventana.setLayout(layout)
ventana.resize(300, 150)
ventana.show()

app.exec()