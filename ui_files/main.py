import sys
import json
import os
import random
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import QTimer

class QuizAleman(QtWidgets.QMainWindow):
    def __init__(self):
        super(QuizAleman, self).__init__()
        
        self.setWindowTitle("Quiz de Alemán A2 - Lückentext")
        self.resize(500, 350)
        
        # Widget central y layout principal
        self.widget_central = QtWidgets.QWidget(self)
        self.setCentralWidget(self.widget_central)
        self.layout = QtWidgets.QVBoxLayout(self.widget_central)
        self.layout.setContentsMargins(30, 30, 30, 30)
        self.layout.setSpacing(15)
        
        # 1. Etiqueta para la pregunta / frase con hueco
        self.label = QtWidgets.QLabel("Cargando pregunta...")
        self.label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.label)
        
        # 2. Caja de texto (QLineEdit) para escribir la respuesta
        self.lineEdit = QtWidgets.QLineEdit()
        self.lineEdit.setStyleSheet("font-size: 14px; padding: 6px;")
        self.lineEdit.setPlaceholderText("Escribe tu respuesta aquí...")
        self.layout.addWidget(self.lineEdit)
        
        # 3. Botón de Comprobar
        self.pushButton = QtWidgets.QPushButton("Comprobar")
        self.pushButton.setStyleSheet("font-size: 14px; padding: 6px; background-color: #0078d7; color: white; font-weight: bold;")
        self.layout.addWidget(self.pushButton)
        
        # 4. Etiqueta para el feedback (Acierto / Fallo)
        self.label_2 = QtWidgets.QLabel("")
        self.label_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_2.setStyleSheet("font-size: 14px;")
        self.layout.addWidget(self.label_2)
        
        # 5. Layout horizontal para los marcadores de aciertos y fallos
        self.layout_marcadores = QtWidgets.QHBoxLayout()
        self.label_aciertos = QtWidgets.QLabel("Richtig: 0")
        self.label_aciertos.setStyleSheet("font-size: 14px; color: green; font-weight: bold;")
        self.label_fallos = QtWidgets.QLabel("Falsch: 0")
        self.label_fallos.setStyleSheet("font-size: 14px; color: red; font-weight: bold;")
        
        self.layout_marcadores.addWidget(self.label_aciertos)
        self.layout_marcadores.addWidget(self.label_fallos)
        self.layout.addLayout(self.layout_marcadores)
        
        # Variables de control
        self.aciertos = 0
        self.fallos = 0
        self.pregunta_actual = None
        
        # Cargar datos del JSON
        self.cargar_datos_json()
        
        # Conectar señales (botones y tecla Enter)
        self.pushButton.clicked.connect(self.verificar_respuesta)
        self.lineEdit.returnPressed.connect(self.verificar_respuesta)
        
        # Arrancar el juego
        self.cargar_nueva_pregunta()

    def cargar_datos_json(self):
        ruta_json = 'vocabulario.json'
        if os.path.exists(ruta_json):
            with open(ruta_json, 'r', encoding='utf-8') as f:
                self.vocabulario = json.load(f)
        else:
            self.vocabulario = [
                {"frase": "Ich ____ ein Buch.", "respuesta": "lese", "pista": "Presente"}
            ]

    def actualizar_marcadores(self):
        self.label_aciertos.setText(f"Richtig: {self.aciertos}")
        self.label_fallos.setText(f"Falsch: {self.fallos}")

    def cargar_nueva_pregunta(self):
        if not self.vocabulario:
            return
            
        self.pregunta_actual = random.choice(self.vocabulario)
        
        texto_label = f"{self.pregunta_actual['frase']}"
        if "pista" in self.pregunta_actual:
            texto_label += f"\n\n💡 Pista: {self.pregunta_actual['pista']}"
            
        self.label.setText(texto_label)
        self.label_2.setText("")
        self.lineEdit.clear()
        self.lineEdit.setFocus()

    def verificar_respuesta(self):
        if not self.pregunta_actual:
            return
            
        respuesta_usuario = self.lineEdit.text().strip()
        respuesta_correcta = self.pregunta_actual['respuesta'].strip()
        
        if respuesta_usuario.lower() == respuesta_correcta.lower():
            self.aciertos += 1
            self.label_2.setText("Richtig! 🎉 ¡Muy bien!")
            self.label_2.setStyleSheet("font-size: 14px; color: green; font-weight: bold;")
            QTimer.singleShot(1200, self.cargar_nueva_pregunta)
        else:
            self.fallos += 1
            self.label_2.setText(f"Falsch ❌ Era: '{respuesta_correcta}'")
            self.label_2.setStyleSheet("font-size: 14px; color: red; font-weight: bold;")
            
        self.actualizar_marcadores()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ventana = QuizAleman()
    ventana.show()
    sys.exit(app.exec())