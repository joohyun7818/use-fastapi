"""Utility script to align the live database schema with the current ORM models."""
from contextlib import contextmanager
from typing import Callable

from sqlalchemy import inspect, text

from kaira_fastapi_poetry.database import engine


@contextmanager
def begin_connection():
    """Yield a connection with an open transaction."""
    with engine.begin() as connection:  # engine.begin() creates and commits/rolls back automatically
        yield connection


def has_column(inspector, table_name: str, column: str) -> bool:
    """Return True if the column exists on the table."""
    return any(col["name"] == column for col in inspector.get_columns(table_name))


def rename_column(connection, table_name: str, source: str, target: str) -> bool:
    if not has_column(inspect(connection), table_name, source):
        return False
    if has_column(inspect(connection), table_name, target):
        return False
    connection.execute(text(f"ALTER TABLE {table_name} RENAME COLUMN {source} TO {target}"))
    return True


def ensure_column(connection, table_name: str, column: str, ddl_supplier: Callable[[], str]) -> bool:
    inspector = inspect(connection)
    if has_column(inspector, table_name, column):
        return False
    ddl = ddl_supplier()
    connection.execute(text(f"ALTER TABLE {table_name} ADD COLUMN {column} {ddl}"))
    return True


def constraint_exists(connection, table_name: str, constraint_name: str) -> bool:
    result = connection.execute(
        text(
            """
            SELECT 1
            FROM information_schema.table_constraints
            WHERE table_name = :table
              AND constraint_name = :name
            """
        ),
        {"table": table_name, "name": constraint_name},
    ).first()
    return result is not None


def drop_constraint(connection, table_name: str, constraint_name: str) -> bool:
    if not constraint_exists(connection, table_name, constraint_name):
        return False
    connection.execute(text(f"ALTER TABLE {table_name} DROP CONSTRAINT {constraint_name}"))
    return True


def main():
    actions = []
    with begin_connection() as conn:
        if rename_column(conn, "users", "password_hash", "hashed_password"):
            actions.append("Renamed users.password_hash -> users.hashed_password")

        if ensure_column(conn, "users", "role", lambda: "VARCHAR(50) NOT NULL DEFAULT 'user'"):
            actions.append("Added users.role column with default 'user'")

        if drop_constraint(conn, "users", "users_username_key"):
            actions.append("Dropped users_username_key constraint for username duplicates")

    if not actions:
        print("Database schema already matches ORM expectations.")
    else:
        print("Applied schema fixes:")
        for action in actions:
            print(f" - {action}")


if __name__ == "__main__":
    main()
