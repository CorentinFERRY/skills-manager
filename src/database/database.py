
import sqlite3

DB_PATH = "skills_manager.db"

def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(conn: sqlite3.Connection) -> None:
    cursor = conn.cursor()
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS learners (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS trainers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS validations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            learner_id INTEGER NOT NULL,
            skill_id INTEGER NOT NULL,
            status TEXT NOT NULL CHECK(status IN ('pre_validated', 'validated')),
            pre_validated_by INTEGER,
            FOREIGN KEY (learner_id) REFERENCES learners(id),
            FOREIGN KEY (skill_id) REFERENCES skills(id),
            FOREIGN KEY (pre_validated_by) REFERENCES learners(id)
        );
    """)
    conn.commit()