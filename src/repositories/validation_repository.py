import sqlite3

from src.database.database import get_connection


def insert_validation(learner_id: int, skill_id: int) -> sqlite3.Row:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO validations (learner_id, skill_id, status, pre_validated_by) VALUES (?, ?, ?, ?)",
        (learner_id, skill_id, "validated", None),
    )
    conn.commit()
    cursor.execute(
        "SELECT id, learner_id, skill_id, status, pre_validated_by FROM validations WHERE id = ?",
        (cursor.lastrowid,),
    )
    return cursor.fetchone()


def insert_pre_validation(
    learner_id: int, skill_id: int, validator_id: int
) -> sqlite3.Row:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO validations (learner_id, skill_id, status, pre_validated_by) VALUES (?, ?, ?, ?)",
        (learner_id, skill_id, "pre_validated", validator_id),
    )
    conn.commit()
    cursor.execute(
        "SELECT id, learner_id, skill_id, status, pre_validated_by FROM validations WHERE id = ?",
        (cursor.lastrowid,),
    )
    return cursor.fetchone()


def find_validated_skills_by_learner(learner_id: int) -> list[sqlite3.Row]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT skill_id FROM validations WHERE learner_id = ? AND status = ?",
        (learner_id, "validated"),
    )
    return cursor.fetchall()
