import sqlite3

def mostrar_menu():
    print("\n--- GESTOR DE VOCABULARIO ALEMÁN ---")
    print("1. Ver total de preguntas en la BD")
    print("2. Añadir una nueva pregunta")
    print("3. Salir")

def gestionar_bd():
    conexion = sqlite3.connect("vocabulario.db")
    cursor = conexion.cursor()
    
    # Asegurar que la tabla existe
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vocabulario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            frase TEXT NOT NULL,
            respuesta TEXT NOT NULL,
            pista TEXT
        )
    """)
    conexion.commit()

    while True:
        mostrar_menu()
        opcion = input("\nElige una opción: ").strip()
        
        if opcion == "1":
            cursor.execute("SELECT COUNT(*) FROM vocabulario")
            total = cursor.fetchone()[0]
            print(f"\n📊 Total de preguntas registradas: {total}")
            
        elif opcion == "2":
            print("\n--- Añadir nueva pregunta (Usa '____' para el hueco) ---")
            frase = input("Frase (ej: Ich ____ ein Buch): ").strip()
            respuesta = input("Respuesta correcta (ej: lese): ").strip()
            pista = input("Pista gramatical (ej: Presente): ").strip()
            
            if frase and respuesta:
                cursor.execute(
                    "INSERT INTO vocabulario (frase, respuesta, pista) VALUES (?, ?, ?)",
                    (frase, respuesta, pista)
                )
                conexion.commit()
                print("✅ ¡Pregunta añadida correctamente a la base de datos!")
            else:
                print("❌ Error: La frase y la respuesta no pueden estar vacías.")
                
        elif opcion == "3":
            print("\nSaliendo del gestor...")
            break
        else:
            print("❌ Opción no válida. Inténtalo de nuevo.")
            
    conexion.close()

if __name__ == "__main__":
gestor_bd()