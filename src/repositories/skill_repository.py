import sqlite3

from src.database.database import get_connection


def find_all() -> list[sqlite3.Row]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM skills")
    return cursor.fetchall()


def find_by_id(skill_id: int) -> sqlite3.Row | None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM skills WHERE id = ?", (skill_id,))
    return cursor.fetchone()


def insert(name: str) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO skills (name) VALUES (?)", (name,))
    conn.commit()
    return cursor.lastrowid  # type: ignore[return-value]


def update(skill_id: int, name: str) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE skills SET name = ? WHERE id = ?", (name, skill_id))
    conn.commit()
    return cursor.rowcount > 0


def delete(skill_id: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM skills WHERE id = ?", (skill_id,))
    conn.commit()
    return cursor.rowcount > 0
