import sys
import random
from PyQt6 import QtWidgets, uic

# Tu vocabulario de alemán a español
VOCABULARIO = {
    "Der Tisch": "La mesa",
    "Der Stuhl": "La silla",
    "Das Fenster": "La ventana",
    "Die Tür": "La puerta",
    "Das Wasser": "El agua",
    "Der Apfel": "La manzana"
}

class QuizAleman(QtWidgets.QMainWindow):
    def __init__(self):
        super(QuizAleman, self).__init__()
        
        # ⚠️ IMPORTANTE: Cambia 'juego_aleman.ui' por el nombre real de tu archivo guardado
        uic.loadUi('juego_aleman.ui', self)
        
        # Agrupamos tus botones utilizando los nombres por defecto que ya tienes
        self.botones = [self.pushButton, self.pushButton_2, self.pushButton_3, self.pushButton_4]
        
        # Conectamos cada botón para que detecte el clic
        for boton in self.botones:
            boton.clicked.connect(self.verificar_respuesta)
            
        self.respuesta_correcta = ""
        self.cargar_nueva_pregunta()

    def cargar_nueva_pregunta(self):
        # Elegimos una palabra aleatoria
        aleman, espanol = random.choice(list(VOCABULARIO.items()))
        self.respuesta_correcta = espanol
        
        # Usamos 'label' (tu etiqueta de arriba) para la pregunta
        self.label.setText(f"¿Qué significa: {aleman}?")
        
        # Preparamos las opciones (1 correcta y 3 incorrectas)
        opciones = [espanol]
        otras = [v for k, v in VOCABULARIO.items() if v != espanol]
        opciones.extend(random.sample(otras, min(3, len(otras))))
        random.shuffle(opciones)
        
        # Asignamos los textos a tus 4 botones
        for i, boton in enumerate(self.botones):
            boton.setText(opciones[i])
            
        # Usamos 'label_2' (tu etiqueta de abajo) para limpiar el resultado previo
        self.label_2.setText("")

    def verificar_respuesta(self):
        boton_pulsado = self.sender()
        
        # Comprobamos si el texto del botón coincide con la respuesta correcta
        if boton_pulsado.text() == self.respuesta_correcta:
            self.label_2.setText("¡Correcto! 🎉 Muy bien.")
        else:
            self.label_2.setText(f"¡Fallaste! Era: {self.respuesta_correcta} ❌")

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ventana = QuizAleman()
    ventana.show()
    sys.exit(app.exec())