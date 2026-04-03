import sqlite3
from src.database.database import get_connection


def find_all() -> list[sqlite3.Row]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nom FROM learners")
    return cursor.fetchall()


def find_by_id(learner_id: int) -> sqlite3.Row | None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, nom FROM learners WHERE id = ?",
        (learner_id,)
    )
    return cursor.fetchone()


def find_validated_skills(learner_id: int) -> list[sqlite3.Row]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT skill_id FROM validations WHERE learner_id = ? AND status = ?",
        (learner_id, "validated")
    )
    return cursor.fetchall()


def insert(nom: str) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO learners (nom) VALUES (?)",
        (nom,)
    )
    conn.commit()
    return cursor.lastrowid  # type: ignore[return-value]


def update(learner_id: int, nom: str) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE learners SET nom = ? WHERE id = ?",
        (nom, learner_id)
    )
    conn.commit()
    return cursor.rowcount > 0


def delete(learner_id: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM learners WHERE id = ?",
        (learner_id,)
    )
    conn.commit()
    return cursor.rowcount > 0