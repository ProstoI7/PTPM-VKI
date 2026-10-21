import sqlite3

class TriangleDatabase:

    def __init__(self, db_path: str = ":memory:"):
        self.db_path = db_path
        self.connection = sqlite3.connect(db_path)
        self.connection.row_factory = sqlite3.Row
        self._create_table()

    def _create_table(self):
        cursor = self.connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS triangles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                side_a REAL NOT NULL,
                side_b REAL NOT NULL,
                side_c REAL NOT NULL,
                triangle_type TEXT NOT NULL,
                error_message TEXT,
                UNIQUE(side_a, side_b, side_c)
            )
        """)
        self.connection.commit()

    def add_record(self, side_a, side_b, side_c, triangle_type, error_message=None):
        cursor = self.connection.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO triangles (side_a, side_b, side_c, triangle_type, error_message) "
            "VALUES (?, ?, ?, ?, ?)",
            (side_a, side_b, side_c, triangle_type, error_message)
        )
        self.connection.commit()
        return cursor.lastrowid

    def get_record(self, side_a, side_b, side_c):
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT * FROM triangles WHERE side_a = ? AND side_b = ? AND side_c = ?",
            (side_a, side_b, side_c)
        )
        row = cursor.fetchone()
        return dict(row) if row else None

    def delete_record(self, side_a, side_b, side_c):
        cursor = self.connection.cursor()
        cursor.execute(
            "DELETE FROM triangles WHERE side_a = ? AND side_b = ? AND side_c = ?",
            (side_a, side_b, side_c)
        )
        self.connection.commit()
        return cursor.rowcount

    def close(self):
        self.connection.close()