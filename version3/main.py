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
        self.resize(500, 420)
        
        self.widget_central = QtWidgets.QWidget(self)
        self.setCentralWidget(self.widget_central)
        self.layout = QtWidgets.QVBoxLayout(self.widget_central)
        self.layout.setContentsMargins(30, 30, 30, 30)
        self.layout.setSpacing(12)
        
        # Cabecera: Progreso y Tiempo
        self.layout_top = QtWidgets.QHBoxLayout()
        self.label_progreso = QtWidgets.QLabel("Pregunta 1 de 10")
        self.label_progreso.setStyleSheet("font-size: 12px; color: gray; font-weight: bold;")
        
        self.label_tiempo = QtWidgets.QLabel("⏱️ Tiempo: 15s")
        self.label_tiempo.setStyleSheet("font-size: 13px; color: #d9534f; font-weight: bold;")
        self.label_tiempo.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        
        self.layout_top.addWidget(self.label_progreso)
        self.layout_top.addWidget(self.label_tiempo)
        self.layout.addLayout(self.layout_top)
        
        # 1. Frase principal
        self.label = QtWidgets.QLabel("Cargando pregunta...")
        self.label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.label)
        
        # 2. Caja de texto
        self.lineEdit = QtWidgets.QLineEdit()
        self.lineEdit.setStyleSheet("font-size: 14px; padding: 6px;")
        self.lineEdit.setPlaceholderText("Escribe tu respuesta aquí...")
        self.layout.addWidget(self.lineEdit)
        
        # 3. Botón Comprobar
        self.pushButton = QtWidgets.QPushButton("Comprobar")
        self.pushButton.setStyleSheet("font-size: 14px; padding: 6px; background-color: #0078d7; color: white; font-weight: bold;")
        self.layout.addWidget(self.pushButton)
        
        # --- NUEVOS BOTONES DE FIN DE PARTIDA (Ocultos al iniciar) ---
        self.layout_fin = QtWidgets.QHBoxLayout()
        
        self.btn_reiniciar = QtWidgets.QPushButton("🔄 Repetir partida")
        self.btn_reiniciar.setStyleSheet("font-size: 14px; padding: 8px; background-color: #5cb85c; color: white; font-weight: bold;")
        self.btn_reiniciar.clicked.connect(self.reiniciar_partida)
        
        self.btn_cerrar = QtWidgets.QPushButton("❌ Cerrar aplicación")
        self.btn_cerrar.setStyleSheet("font-size: 14px; padding: 8px; background-color: #d9534f; color: white; font-weight: bold;")
        self.btn_cerrar.clicked.connect(self.close)
        
        self.layout_fin.addWidget(self.btn_reiniciar)
        self.layout_fin.addWidget(self.btn_cerrar)
        
        # Añadimos los botones de fin al layout principal pero ocultos
        self.layout.addLayout(self.layout_fin)
        self.btn_reiniciar.hide()
        self.btn_cerrar.hide()
        # -------------------------------------------------------------
        
        # 4. Feedback
        self.label_2 = QtWidgets.QLabel("")
        self.label_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_2.setStyleSheet("font-size: 14px;")
        self.layout.addWidget(self.label_2)
        
        # 5. Marcadores
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
        self.ronda_actual = 0
        self.MAX_PREGUNTAS = 10
        
        # Temporizador
        self.tiempo_restante = 15
        self.timer_cuenta_atras = QTimer(self)
        self.timer_cuenta_atras.timeout.connect(self.actualizar_tiempo)
        
        self.cargar_datos_json()
        
        self.pushButton.clicked.connect(self.verificar_respuesta)
        self.lineEdit.returnPressed.connect(self.verificar_respuesta)
        
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
        if self.ronda_actual >= self.MAX_PREGUNTAS:
            self.mostrar_fin_partida()
            return
            
        self.ronda_actual += 1
        self.label_progreso.setText(f"Pregunta {self.ronda_actual} de {self.MAX_PREGUNTAS}")
        
        self.pregunta_actual = random.choice(self.vocabulario)
        
        texto_label = f"{self.pregunta_actual['frase']}"
        if "pista" in self.pregunta_actual:
            texto_label += f"\n\n💡 Pista: {self.pregunta_actual['pista']}"
            
        self.label.setText(texto_label)
        self.label_2.setText("")
        self.lineEdit.clear()
        self.lineEdit.setFocus()
        self.lineEdit.setEnabled(True)
        self.pushButton.setEnabled(True)
        
        self.tiempo_restante = 15
        self.label_tiempo.setText(f"⏱️ Tiempo: {self.tiempo_restante}s")
        self.timer_cuenta_atras.start(1000)

    def actualizar_tiempo(self):
        self.tiempo_restante -= 1
        self.label_tiempo.setText(f"⏱️ Tiempo: {self.tiempo_restante}s")
        
        if self.tiempo_restante <= 0:
            self.timer_cuenta_atras.stop()
            self.fallos += 1
            respuesta_correcta = self.pregunta_actual['respuesta']
            self.label_2.setText(f"⏰ ¡Tiempo agotado! Era: '{respuesta_correcta}'")
            self.label_2.setStyleSheet("font-size: 14px; color: red; font-weight: bold;")
            self.actualizar_marcadores()
            
            self.lineEdit.setEnabled(False)
            self.pushButton.setEnabled(False)
            QTimer.singleShot(1600, self.cargar_nueva_pregunta)

    def verificar_respuesta(self):
        if not self.pregunta_actual:
            return
            
        self.timer_cuenta_atras.stop()
        
        respuesta_usuario = self.lineEdit.text().strip()
        respuesta_correcta = self.pregunta_actual['respuesta'].strip()
        
        if respuesta_usuario.lower() == respuesta_correcta.lower():
            self.aciertos += 1
            self.label_2.setText("Richtig! 🎉 ¡Muy bien!")
            self.label_2.setStyleSheet("font-size: 14px; color: green; font-weight: bold;")
        else:
            self.fallos += 1
            self.label_2.setText(f"Falsch ❌ Era: '{respuesta_correcta}'")
            self.label_2.setStyleSheet("font-size: 14px; color: red; font-weight: bold;")
            
        self.actualizar_marcadores()
        self.lineEdit.setEnabled(False)
        self.pushButton.setEnabled(False)
        
        QTimer.singleShot(1400, self.cargar_nueva_pregunta)

    def mostrar_fin_partida(self):
        self.timer_cuenta_atras.stop()
        self.label.setText(f"🎯 ¡Ronda Finalizada!\nAciertos: {self.aciertos} | Fallos: {self.fallos}")
        self.label_progreso.setText("¡Completado!")
        self.label_tiempo.setText("")
        
        # Ocultamos elementos de juego activo
        self.lineEdit.hide()
        self.pushButton.hide()
        
        # Mostramos los botones de fin de partida
        self.btn_reiniciar.show()
        self.btn_cerrar.show()
        
        self.label_2.setText("¿Qué deseas hacer ahora?")
        self.label_2.setStyleSheet("font-size: 14px; color: #333; font-weight: bold;")

    def reiniciar_partida(self):
        # Reseteamos contadores y variables
        self.aciertos = 0
        self.fallos = 0
        self.ronda_actual = 0
        self.actualizar_marcadores()
        
        # Ocultamos botones de fin y volvemos a mostrar la caja de texto y comprobar
        self.btn_reiniciar.hide()
        self.btn_cerrar.hide()
        self.lineEdit.show()
        self.pushButton.show()
        
        # Arrancamos nueva ronda
        self.cargar_nueva_pregunta()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ventana = QuizAleman()
    ventana.show()
    sys.exit(app.exec())