import sqlite3

from src.database.database import get_connection
from src.repositories.validation_repository import find_validated_skills_by_learner


def find_all() -> list[sqlite3.Row]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM learners")
    return cursor.fetchall()


def find_by_id(learner_id: int) -> sqlite3.Row | None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM learners WHERE id = ?", (learner_id,))
    return cursor.fetchone()


def find_validated_skills(learner_id: int) -> list[sqlite3.Row]:
    return find_validated_skills_by_learner(learner_id)


def insert(name: str) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO learners (name) VALUES (?)", (name,))
    conn.commit()
    return cursor.lastrowid  # type: ignore[return-value]


def update(learner_id: int, name: str) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE learners SET name = ? WHERE id = ?", (name, learner_id))
    conn.commit()
    return cursor.rowcount > 0


def delete(learner_id: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM learners WHERE id = ?", (learner_id,))
    conn.commit()
    return cursor.rowcount > 0
