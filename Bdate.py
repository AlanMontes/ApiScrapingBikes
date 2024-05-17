import sqlite3
import csv

def create_bikes_table():
 # Conexión a la base de datos "hot100.db"
 conn = sqlite3.connect("hot100.db")
 # Crear un cursor para interactuar con la base de datos
 cursor = conn.cursor()
 # Crear la tabla "bikes" si no existe
 cursor.execute("""CREATE TABLE IF NOT EXISTS bikes(
 id INTEGER PRIMARY KEY,
 bicicleta TEXT,
 precio TEXT ,
 especificaciones TEXT,
 categoria TEXT
 )
 """)
 
 # Confirmar los cambios en la base de datos y cerrar la conexión
 conn.commit()
 conn.close()

def read_csv_file(csv_file):
 # Leer el archivo CSV y guardar los datos en una lista de diccionarios
 with open(csv_file, newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    data = [row for row in reader]
 return data


def insert_data_to_ranking_table(data):
 # Conexión a la base de datos "hot100.db"
 conn = sqlite3.connect("hot100.db")
 # Crear un cursor para interactuar con la base de datos
 cursor = conn.cursor()
 # Insertar cada fila de datos en la tabla "ranking"
 for row in data:
    cursor.execute("""
    INSERT INTO bikes (bicicleta, precio, especificaciones,categoria)
    VALUES (?, ?, ?, ?)
    """, (row["\ufeffBicicleta"], row["Precio"], row["Especificaciones"], row["categoria"]))
 # Confirmar los cambios en la base de datos y cerrar la conexión
 conn.commit()
 conn.close()



if __name__ == "__main__":
 # Nombre del archivo CSV que contiene los datos
 csv_file = "bikes_data.csv"
 
 # Leer los datos del archivo CSV y guardarlos en una lista de diccionarios
 data_to_insert = read_csv_file(csv_file)
 
 # Crear la tabla "bikes" en la base de datos "hot100.db"
 create_bikes_table()
 
 # Insertar los datos en la tabla "ranking" desde el archivo CSV
 insert_data_to_ranking_table(data_to_insert)
