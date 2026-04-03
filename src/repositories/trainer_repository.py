import sqlite3
from src.database.database import get_connection


def find_all() -> list[sqlite3.Row]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM trainers")
    return cursor.fetchall()


def find_by_id(trainer_id: int) -> sqlite3.Row | None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, name FROM trainers WHERE id = ?",
        (trainer_id,)
    )
    return cursor.fetchone()


def insert(name: str) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO trainers (name) VALUES (?)",
        (name,)
    )
    conn.commit()
    return cursor.lastrowid  # type: ignore[return-value]


def update(trainer_id: int, name: str) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE trainers SET name = ? WHERE id = ?",
        (name, trainer_id)
    )
    conn.commit()
    return cursor.rowcount > 0


def delete(trainer_id: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM trainers WHERE id = ?",
        (trainer_id,)
    )
    conn.commit()
    return cursor.rowcount > 0