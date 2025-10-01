import sqlite3


class DB:
    def __init__(self):
        self.DB_FILE = "weather.db"


    def DbTableCreation(self):
        conn=self.DbConnection()
        cursor = conn.cursor()
        # Create table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS weather_info (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                lattitude REAL,
                longitude REAL,
                temperature_2m text,
                relative_humidity_2m text,
                timestamp text
            )
        ''')

        conn.commit()
        conn.close()
    
    def DbConnection(self):
        conn = sqlite3.connect(self.DB_FILE)
        return conn