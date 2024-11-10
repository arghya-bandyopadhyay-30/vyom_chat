import sqlite3
from datetime import datetime


class ChatHistory:
    def __init__(self, db_path="chat_history.db"):
        self.db_path = db_path
        self.__create_table()

    def __create_table(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS chat_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    user_message TEXT,
                    assistant_response TEXT
                )
            ''')
            conn.commit()

    def add_message(self, user_message: str, assistant_response: str):
        timestamp = datetime.now().isoformat()
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO chat_history (timestamp, user_message, assistant_response)
                VALUES (?, ?, ?)
            ''', (timestamp, user_message, assistant_response))
            conn.commit()

    def get_history(self, limit=10):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT timestamp, user_message, assistant_response 
                FROM chat_history 
                ORDER BY id DESC 
                LIMIT ?
            ''', (limit,))
            return cursor.fetchall()

    def clear_history(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM chat_history')
            conn.commit()

