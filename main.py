import sys
import sqlite3
import random
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import QTimer

class QuizAleman(QtWidgets.QMainWindow):
    def __init__(self):
        super(QuizAleman, self).__init__()
        
        self.setWindowTitle("App de Alemán A2 - SQLite Edition")
        self.resize(600, 520)
        
        # Inicializar Base de Datos primero
        self.inicializar_base_datos()
        
        # Widget principal con Pestañas (Tabs)
        self.tabs = QtWidgets.QTabWidget()
        self.setCentralWidget(self.tabs)
        
        # Crear las dos vistas principales
        self.tab_quiz = QtWidgets.QWidget()
        self.tab_gestor = QtWidgets.QWidget()
        
        self.tabs.addTab(self.tab_quiz, "🎮 Practicar (Quiz)")
        self.tabs.addTab(self.tab_gestor, "📚 Gestionar Base de Datos")
        
        # Configurar cada pestaña
        self.setup_ui_quiz()
        self.setup_ui_gestor()
        
        # Variables de control del Quiz
        self.aciertos = 0
        self.fallos = 0
        self.pregunta_actual = None 
        self.ronda_actual = 0
        self.MAX_PREGUNTAS = 10
        
        # Temporizador
        self.tiempo_restante = 15
        self.timer_cuenta_atras = QTimer(self)
        self.timer_cuenta_atras.timeout.connect(self.actualizar_tiempo)
        
        # Arrancar primera pregunta
        self.cargar_nueva_pregunta()

    def inicializar_base_datos(self):
        self.conexion = sqlite3.connect("vocabulario.db")
        self.cursor = self.conexion.cursor()
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS vocabulario (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                kapitel TEXT DEFAULT 'Kapitel 1',
                frase TEXT NOT NULL,
                respuesta TEXT NOT NULL,
                pista TEXT
            )
        """)
        self.conexion.commit()
        
        # Migración por si la tabla era antigua
        self.cursor.execute("PRAGMA table_info(vocabulario)")
        columnas = [col[1] for col in self.cursor.fetchall()]
        if "kapitel" not in columnas:
            self.cursor.execute("ALTER TABLE vocabulario ADD COLUMN kapitel TEXT DEFAULT 'Kapitel 1'")
            self.conexion.commit()
            
        # Comprobar si está vacía para insertar datos iniciales estructurados
        self.cursor.execute("SELECT COUNT(*) FROM vocabulario")
        count = self.cursor.fetchone()[0]
        
        if count < 15:
            self.cursor.execute("DELETE FROM vocabulario")
            self.conexion.commit()
            
            datos_iniciales = [
                ("Kapitel 1", "Gestern ____ ich bis zehn Uhr geschlafen.", "habe", "Perfekt con haben"),
                ("Kapitel 1", "Am Wochenende ____ wir nach Berlin gefahren.", "sind", "Perfekt con sein (movimiento)"),
                ("Kapitel 1", "Was ____ du gestern Abend gemacht?", "hast", "Pregunta en Perfekt"),
                ("Kapitel 1", "Um wie viel Uhr ____ ihr gestern angekommen?", "seid", "Perfekt con sein (llegada)"),
                ("Kapitel 1", "Ich lerne Deutsch, ____ ich in Deutschland arbeiten möchte.", "weil", "Subordinada causal (verbo al final)"),
                ("Kapitel 1", "Er kann heute nicht kommen, ____ er krank ist.", "weil", "Justificar ausencia"),
                ("Kapitel 1", "Wir ____ gestern ins Kino gehen, aber keine Zeit.", "wollten", "Verbo modal Präteritum (wollten)"),
                ("Kapitel 1", "Wollen wir uns morgen um drei Uhr ____?", "treffen", "Sich verabreden / Quedar"),
                ("Kapitel 1", "Hast du am Freitag Zeit? – Ja, sehr ____!", "gerne", "Aceptar una cita"),
                ("Kapitel 1", "Tut mir leid, ich habe heute ____ Zeit.", "keine", "Rechazar un plan educadamente"),
                
                ("Kapitel 2", "Als ich Kind war, ____ ich oft im Park gespielt.", "hatte", "Präteritum de haben"),
                ("Kapitel 2", "Früher ____ wir in einer kleinen Wohnung gewohnt.", "wohnten", "Präteritum regular"),
                ("Kapitel 2", "Mein Kollege ist sehr nett, ____ er immer pünktlich ist.", "weil", "Conectores causales"),
                ("Kapitel 2", "Ich arbeite als Grafiker, ____ mir Design Spaß macht.", "weil", "Motivo laboral"),
                ("Kapitel 2", "Letztes Jahr ____ ich nach München umgezogen.", "bin", "Perfekt cambio de lugar"),
                ("Kapitel 2", "Wo ____ du im letzten Sommer im Urlaub?", "warst", "Präteritum de sein"),
                
                ("Grammatik A2", "Das Buch, ____ auf dem Tisch liegt, ist interessant.", "das", "Relativpronomen (Neutrum)"),
                ("Grammatik A2", "Der Mann, ____ dort drüben steht, ist mein Chef.", "der", "Relativpronomen (Maskulinum)"),
                ("Grammatik A2", "Ich kenne die Frau, ____ Auto gestohlen wurde.", "deren", "Genitiv Relativpronomen"),
                ("Grammatik A2", "Wegen ____ schlechten Wetters sind wir zu Hause geblieben.", "des", "Genitivpräposition wegen")
            ]
            self.cursor.executemany("INSERT INTO vocabulario (kapitel, frase, respuesta, pista) VALUES (?, ?, ?, ?)", datos_iniciales)
            self.conexion.commit()

    def setup_ui_quiz(self):
        layout = QtWidgets.QVBoxLayout(self.tab_quiz)
        layout.setContentsMargins(30, 20, 30, 30)
        layout.setSpacing(15)
        
        # Panel superior de selección de lección con diseño limpio
        group_box = QtWidgets.QGroupBox("Configuración de la partida")
        group_layout = QtWidgets.QHBoxLayout()
        
        self.label_sel_kapitel = QtWidgets.QLabel("📚 Seleccionar Lección:")
        self.label_sel_kapitel.setStyleSheet("font-weight: bold;")
        
        self.combo_kapitel = QtWidgets.QComboBox()
        self.combo_kapitel.addItem("Todos los capítulos (Mix)")
        self.combo_kapitel.addItem("Kapitel 1: Rund ums Leben")
        self.combo_kapitel.addItem("Kapitel 2: Arbeit und Beruf")
        self.combo_kapitel.addItem("Grammatik A2 (Mix)")
        self.combo_kapitel.setStyleSheet("padding: 5px;")
        self.combo_kapitel.currentIndexChanged.connect(self.reiniciar_partida)
        
        group_layout.addWidget(self.label_sel_kapitel)
        group_layout.addWidget(self.combo_kapitel)
        group_box.setLayout(group_layout)
        layout.addWidget(group_box)

        # Cabecera de estado: Progreso y Tiempo
        layout_top = QtWidgets.QHBoxLayout()
        self.label_progreso = QtWidgets.QLabel("Pregunta 1 de 10")
        self.label_progreso.setStyleSheet("font-size: 13px; color: #555; font-weight: bold;")
        
        self.label_tiempo = QtWidgets.QLabel("⏱️ Tiempo: 15s")
        self.label_tiempo.setStyleSheet("font-size: 13px; color: #d9534f; font-weight: bold;")
        self.label_tiempo.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        
        layout_top.addWidget(self.label_progreso)
        layout_top.addWidget(self.label_tiempo)
        layout.addLayout(layout_top)
        
        # Frase principal del Quiz
        self.label = QtWidgets.QLabel("Cargando pregunta...")
        self.label.setWordWrap(True)
        self.label.setStyleSheet("font-size: 16px; font-weight: bold; background-color: #f8f9fa; padding: 15px; border-radius: 5px; border: 1px solid #ddd;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)
        
        # Entrada de respuesta
        self.lineEdit = QtWidgets.QLineEdit()
        self.lineEdit.setStyleSheet("font-size: 15px; padding: 8px;")
        self.lineEdit.setPlaceholderText("Escribe la palabra que falta...")
        layout.addWidget(self.lineEdit)
        
        # Botón Comprobar
        self.pushButton = QtWidgets.QPushButton("Comprobar Respuesta")
        self.pushButton.setStyleSheet("font-size: 14px; padding: 10px; background-color: #0078d7; color: white; font-weight: bold; border-radius: 4px;")
        layout.addWidget(self.pushButton)
        
        # Botones de fin de partida (Ocultos al iniciar)
        self.layout_fin = QtWidgets.QHBoxLayout()
        self.btn_reiniciar = QtWidgets.QPushButton("🔄 Repetir partida")
        self.btn_reiniciar.setStyleSheet("font-size: 14px; padding: 8px; background-color: #5cb85c; color: white; font-weight: bold;")
        self.btn_reiniciar.clicked.connect(self.reiniciar_partida)
        
        self.btn_cerrar = QtWidgets.QPushButton("❌ Salir")
        self.btn_cerrar.setStyleSheet("font-size: 14px; padding: 8px; background-color: #d9534f; color: white; font-weight: bold;")
        self.btn_cerrar.clicked.connect(self.close)
        
        self.layout_fin.addWidget(self.btn_reiniciar)
        self.layout_fin.addWidget(self.btn_cerrar)
        layout.addLayout(self.layout_fin)
        self.btn_reiniciar.hide()
        self.btn_cerrar.hide()
        
        # Feedback visual de acierto/fallo
        self.label_2 = QtWidgets.QLabel("")
        self.label_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_2.setStyleSheet("font-size: 14px;")
        layout.addWidget(self.label_2)
        
        # Marcadores inferiores
        layout_marcadores = QtWidgets.QHBoxLayout()
        self.label_aciertos = QtWidgets.QLabel("Richtig: 0")
        self.label_aciertos.setStyleSheet("font-size: 14px; color: #28a745; font-weight: bold;")
        self.label_fallos = QtWidgets.QLabel("Falsch: 0")
        self.label_fallos.setStyleSheet("font-size: 14px; color: #dc3545; font-weight: bold;")
        
        layout_marcadores.addWidget(self.label_aciertos)
        layout_marcadores.addWidget(self.label_fallos)
        layout.addLayout(layout_marcadores)
        
        # Conexiones de eventos del quiz
        self.pushButton.clicked.connect(self.verificar_respuesta)
        self.lineEdit.returnPressed.connect(self.verificar_respuesta)

    def setup_ui_gestor(self):
        layout = QtWidgets.QVBoxLayout(self.tab_gestor)
        layout.setContentsMargins(20, 20, 20, 20)
        
        label_info = QtWidgets.QLabel("📋 Listado actual de preguntas almacenadas en SQLite:")
        label_info.setStyleSheet("font-weight: bold; font-size: 13px;")
        layout.addWidget(label_info)
        
        # Tabla para mostrar el contenido de la base de datos
        self.tabla_vocabulario = QtWidgets.QTableWidget()
        self.tabla_vocabulario.setColumnCount(5)
        self.tabla_vocabulario.setHorizontalHeaderLabels(["ID", "Capítulo", "Frase", "Respuesta", "Pista"])
        self.tabla_vocabulario.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.tabla_vocabulario)
        
        btn_actualizar_tabla = QtWidgets.QPushButton("🔄 Recargar datos de la tabla")
        btn_actualizar_tabla.setStyleSheet("padding: 8px; font-weight: bold; background-color: #6c757d; color: white;")
        btn_actualizar_tabla.clicked.connect(self.cargar_datos_en_tabla)
        layout.addWidget(btn_actualizar_tabla)
        
        # Cargar datos inicialmente
        self.cargar_datos_en_tabla()

    def cargar_datos_en_tabla(self):
        self.cursor.execute("SELECT id, kapitel, frase, respuesta, pista FROM vocabulario")
        registros = self.cursor.fetchall()
        
        self.tabla_vocabulario.setRowCount(len(registros))
        for row_idx, row_data in enumerate(registros):
            for col_idx, data in enumerate(row_data):
                item = QtWidgets.QTableWidgetItem(str(data))
                self.tabla_vocabulario.setItem(row_idx, col_idx, item)

    def actualizar_marcadores(self):
        self.label_aciertos.setText(f"Richtig: {self.aciertos}")
        self.label_fallos.setText(f"Falsch: {self.fallos}")

    def cargar_nueva_pregunta(self):
        if self.ronda_actual >= self.MAX_PREGUNTAS:
            self.mostrar_fin_partida()
            return
            
        self.ronda_actual += 1
        self.label_progreso.setText(f"Pregunta {self.ronda_actual} de {self.MAX_PREGUNTAS}")
        
        seleccion = self.combo_kapitel.currentText()
        
        if "Kapitel 1" in seleccion:
            self.cursor.execute("SELECT id, frase, respuesta, pista FROM vocabulario WHERE kapitel = 'Kapitel 1' ORDER BY RANDOM() LIMIT 1")
        elif "Kapitel 2" in seleccion:
            self.cursor.execute("SELECT id, frase, respuesta, pista FROM vocabulario WHERE kapitel = 'Kapitel 2' ORDER BY RANDOM() LIMIT 1")
        elif "Grammatik" in seleccion:
            self.cursor.execute("SELECT id, frase, respuesta, pista FROM vocabulario WHERE kapitel = 'Grammatik A2' ORDER BY RANDOM() LIMIT 1")
        else:
            self.cursor.execute("SELECT id, frase, respuesta, pista FROM vocabulario ORDER BY RANDOM() LIMIT 1")
            
        self.pregunta_actual = self.cursor.fetchone()
        
        if not self.pregunta_actual:
            self.label.setText("⚠️ No hay suficientes preguntas para este filtro.")
            self.lineEdit.setEnabled(False)
            self.pushButton.setEnabled(False)
            return
            
        frase = self.pregunta_actual[1]
        pista = self.pregunta_actual[3]
        
        texto_label = f"{frase}"
        if pista:
            texto_label += f"\n\n💡 Pista: {pista}"
            
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
            respuesta_correcta = self.pregunta_actual[2]
            self.label_2.setText(f"⏰ ¡Tiempo agotado! Era: '{respuesta_correcta}'")
            self.label_2.setStyleSheet("font-size: 14px; color: #dc3545; font-weight: bold;")
            self.actualizar_marcadores()
            
            self.lineEdit.setEnabled(False)
            self.pushButton.setEnabled(False)
            QTimer.singleShot(1600, self.cargar_nueva_pregunta)

    def verificar_respuesta(self):
        if not self.pregunta_actual:
            return
            
        self.timer_cuenta_atras.stop()
        
        respuesta_usuario = self.lineEdit.text().strip()
        respuesta_correcta = self.pregunta_actual[2].strip()
        
        if respuesta_usuario.lower() == respuesta_correcta.lower():
            self.aciertos += 1
            self.label_2.setText("Richtig! 🎉 ¡Muy bien!")
            self.label_2.setStyleSheet("font-size: 14px; color: #28a745; font-weight: bold;")
        else:
            self.fallos += 1
            self.label_2.setText(f"Falsch ❌ Era: '{respuesta_correcta}'")
            self.label_2.setStyleSheet("font-size: 14px; color: #dc3545; font-weight: bold;")
            
        self.actualizar_marcadores()
        self.lineEdit.setEnabled(False)
        self.pushButton.setEnabled(False)
        
        QTimer.singleShot(1400, self.cargar_nueva_pregunta)

    def mostrar_fin_partida(self):
        self.timer_cuenta_atras.stop()
        self.label.setText(f"🎯 ¡Ronda Finalizada!\nAciertos: {self.aciertos} | Fallos: {self.fallos}")
        self.label_progreso.setText("¡Completado!")
        self.label_tiempo.setText("")
        
        self.lineEdit.hide()
        self.pushButton.hide()
        
        self.btn_reiniciar.show()
        self.btn_cerrar.show()
        
        self.label_2.setText("¿Qué deseas hacer ahora?")
        self.label_2.setStyleSheet("font-size: 14px; color: #333; font-weight: bold;")

    def reiniciar_partida(self):
        self.aciertos = 0
        self.fallos = 0
        self.ronda_actual = 0
        self.actualizar_marcadores()
        
        self.btn_reiniciar.hide()
        self.btn_cerrar.hide()
        self.lineEdit.show()
        self.pushButton.show()
        
        self.cargar_nueva_pregunta()

    def closeEvent(self, event):
        if hasattr(self, 'conexion'):
            self.conexion.close()
        event.accept()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ventana = QuizAleman()
    ventana.show()
    sys.exit(app.exec())