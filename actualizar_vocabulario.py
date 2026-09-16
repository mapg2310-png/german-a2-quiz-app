import sqlite3

def actualizar_kapitel_1():
    conexion = sqlite3.connect("vocabulario.db")
    cursor = conexion.cursor()
    
    # 1. Comprobamos si la tabla ya existe y si tiene la columna 'kapitel'
    cursor.execute("PRAGMA table_info(vocabulario)")
    columnas = [col[1] for col in cursor.fetchall()]
    
    if "kapitel" not in columnas:
        print("🔄 Actualizando estructura de la base de datos para añadir 'kapitel'...")
        # Si la tabla era antigua, la adaptamos de forma segura o la recreamos
        cursor.execute("DROP TABLE IF EXISTS vocabulario")
    
    # 2. Creamos la tabla con soporte para lecciones
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vocabulario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kapitel TEXT NOT NULL,
            frase TEXT NOT NULL,
            respuesta TEXT NOT NULL,
            pista TEXT
        )
    """)
    
    # 3. Datos específicos del Kapitel 1 (Rund ums Leben)
    preguntas_kapitel_1 = [
        ("Kapitel 1", "Gestern ____ ich bis zehn Uhr geschlafen.", "habe", "Perfekt con haben"),
        ("Kapitel 1", "Am Wochenende ____ wir nach Berlin gefahren.", "sind", "Perfekt con sein (movimiento)"),
        ("Kapitel 1", "Was ____ du gestern Abend gemacht?", "hast", "Pregunta en Perfekt"),
        ("Kapitel 1", "Um wie viel Uhr ____ ihr gestern angekommen?", "seid", "Perfekt con sein (llegada)"),
        ("Kapitel 1", "Ich ____ gestern einen Kuchen gebacken.", "habe", "Actividad cotidiana en Perfekt"),
        ("Kapitel 1", "Ich lerne Deutsch, ____ ich in Deutschland arbeiten möchte.", "weil", "Subordinada causal (verbo al final)"),
        ("Kapitel 1", "Er kann heute nicht kommen, ____ er krank ist.", "weil", "Justificar ausencia"),
        ("Kapitel 1", "Wir bleiben zu Hause, ____ das Wetter schlecht ist.", "weil", "Explicar un cambio de planes"),
        ("Kapitel 1", "Wir ____ gestern ins Kino gehen, aber keine Zeit.", "wollten", "Verbo modal Präteritum (wollen)"),
        ("Kapitel 1", "Was ____ du gestern machen?", "wolltest", "Präteritum de wollen (tú)"),
        ("Kapitel 1", "Leider ____ wir das Ticket nicht kaufen.", "konnten", "Imposibilidad pasada (können)"),
        ("Kapitel 1", "Wollen wir uns morgen um drei Uhr ____?", "treffen", "Sich verabreden / Quedar"),
        ("Kapitel 1", "Hast du am Freitag Zeit? – Ja, sehr ____!", "gerne", "Aceptar una cita"),
        ("Kapitel 1", "Tut mir leid, ich habe heute ____ Zeit.", "keine", "Rechazar un plan educadamente")
    ]
    
    # Insertamos evitando duplicados por frase
    insertadas = 0
    for kapitel, frase, respuesta, pista in preguntas_kapitel_1:
        cursor.execute("SELECT COUNT(*) FROM vocabulario WHERE frase = ?", (frase,))
        if cursor.fetchone()[0] == 0:
            cursor.execute(
                "INSERT INTO vocabulario (kapitel, frase, respuesta, pista) VALUES (?, ?, ?, ?)",
                (kapitel, frase, respuesta, pista)
            )
            insertadas += 1
            
    conexion.commit()
    
    # Estadísticas finales
    cursor.execute("SELECT COUNT(*) FROM vocabulario WHERE kapitel = 'Kapitel 1'")
    total_k1 = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM vocabulario")
    total_general = cursor.fetchone()[0]
    
    conexion.close()
    
    print(f"✅ ¡Base de datos actualizada con éxito!")
    print(f"📖 Preguntas añadidas para Kapitel 1: {insertadas}")
    print(f"📊 Total de preguntas en Kapitel 1: {total_k1}")
    print(f"📈 Total general en la base de datos: {total_general}")

if __name__ == "__main__":
    actualizar_kapitel_1()