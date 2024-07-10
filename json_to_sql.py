import json
import sqlite3

def json_to_sqlite(json_file, sqlite_file):
    # JSON-Datei laden
    with open(json_file, 'r') as file:
        data = json.load(file)

    # Verbindung zur SQLite-Datenbank herstellen
    conn = sqlite3.connect(sqlite_file)
    cursor = conn.cursor()

    # Tabellen erstellen
    cursor.execute('''CREATE TABLE IF NOT EXISTS recipes (
                        id INTEGER PRIMARY KEY,
                        recipe TEXT,
                        time INTEGER,
                        red INTEGER,
                        blue INTEGER,
                        green INTEGER)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS dispensers (
                        id INTEGER PRIMARY KEY,
                        dispenser TEXT,
                        bottle TEXT,
                        time INTEGER,
                        fill_level_grams REAL,
                        recipe INTEGER)''')

    # Daten einfügen
    for key, value in data.items():
        if key == "iot1/teaching_factory_fast/recipe":
            for record_id, record in value.items():
                cursor.execute('''INSERT INTO recipes (id, recipe, time, red, blue, green)
                                  VALUES (?, ?, ?, ?, ?, ?)''', 
                               (int(record_id), 
                                record['recipe'], 
                                record['time'], 
                                record['color_levels_grams']['red'], 
                                record['color_levels_grams']['blue'], 
                                record['color_levels_grams']['green']))
        elif key == "iot1/teaching_factory_fast/dispenser_red":
            for record_id, record in value.items():
                cursor.execute('''INSERT INTO dispensers (id, dispenser, bottle, time, fill_level_grams, recipe)
                                  VALUES (?, ?, ?, ?, ?, ?)''', 
                               (int(record_id), 
                                record['dispenser'], 
                                record['bottle'], 
                                record['time'], 
                                record['fill_level_grams'], 
                                record['recipe']))

    # Änderungen speichern und Verbindung schließen
    conn.commit()
    conn.close()

# Beispielaufruf der Funktion
json_file = 'data.json'  # Pfad zur TinyDB JSON-Datei
sqlite_file = 'data.db'  # Pfad zur SQLite-Datenbank
json_to_sqlite(json_file, sqlite_file)
