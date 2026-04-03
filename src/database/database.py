import sqlite3

DB_PATH = "skills_manager.db"

_connection: sqlite3.Connection


def get_connection() -> sqlite3.Connection:
    global _connection
    if _connection is None:
        _connection = sqlite3.connect(DB_PATH, check_same_thread=False)
        _connection.row_factory = sqlite3.Row
    return _connection


def init_db(conn: sqlite3.Connection) -> None:
    cursor = conn.cursor()
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS learners (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS trainers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
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


def set_connection(conn: sqlite3.Connection) -> None:
    global _connection
    _connection = conn
