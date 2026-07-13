import sqlite3
import os
import logging
from datetime import datetime
from config import CONFIG

logger = logging.getLogger("App")

class DatabaseManager:
    """Handles SQLite operations for enterprise metrics and document tracking."""
    
    def __init__(self):
        self.db_path = os.path.join(CONFIG.BASE_DIR, "enterprise.db")
        self._init_db()

    def _get_conn(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        try:
            with self._get_conn() as conn:
                conn.execute('''CREATE TABLE IF NOT EXISTS documents 
                                (id INTEGER PRIMARY KEY, filename TEXT, upload_date TEXT, 
                                file_size REAL, chunks INTEGER)''')
                conn.execute('''CREATE TABLE IF NOT EXISTS statistics 
                                (id INTEGER PRIMARY KEY, total_queries INTEGER, avg_time REAL)''')
                
                # Initialize stats if empty
                cursor = conn.execute("SELECT COUNT(*) FROM statistics")
                if cursor.fetchone()[0] == 0:
                    conn.execute("INSERT INTO statistics (total_queries, avg_time) VALUES (0, 0.0)")
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")

    def add_document(self, filename: str, file_size_mb: float, chunks: int):
        with self._get_conn() as conn:
            date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            conn.execute("INSERT INTO documents (filename, upload_date, file_size, chunks) VALUES (?, ?, ?, ?)",
                         (filename, date_str, file_size_mb, chunks))

    def get_all_documents(self) -> list:
        with self._get_conn() as conn:
            cursor = conn.execute("SELECT filename, upload_date, file_size, chunks FROM documents")
            return cursor.fetchall()

    def clear_documents(self):
        with self._get_conn() as conn:
            conn.execute("DELETE FROM documents")

    def update_statistics(self, query_time: float):
        with self._get_conn() as conn:
            cursor = conn.execute("SELECT total_queries, avg_time FROM statistics WHERE id = 1")
            row = cursor.fetchone()
            if row:
                t_queries, avg_t = row
                new_total = t_queries + 1
                new_avg = ((avg_t * t_queries) + query_time) / new_total
                conn.execute("UPDATE statistics SET total_queries = ?, avg_time = ? WHERE id = 1", 
                             (new_total, new_avg))

    def get_statistics(self) -> dict:
        with self._get_conn() as conn:
            cursor = conn.execute("SELECT total_queries, avg_time FROM statistics WHERE id = 1")
            row = cursor.fetchone()
            return {"queries": row[0], "avg_time": round(row[1], 2)} if row else {"queries": 0, "avg_time": 0.0}

db = DatabaseManager()