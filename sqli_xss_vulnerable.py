"""Intentionally vulnerable SQL injection and reflected XSS demonstration."""

import sqlite3


def find_user(connection: sqlite3.Connection, username: str) -> list[tuple]:
    """Look up users using intentionally unsafe SQL string interpolation."""
    query = f"SELECT id, username FROM users WHERE username = '{username}'"
    return connection.execute(query).fetchall()


def render_greeting(name: str) -> str:
    """Render user input into HTML without output encoding."""
    return f"<h1>Welcome, {name}!</h1>"


def create_demo_database() -> sqlite3.Connection:
    """Create a small in-memory database for local demonstrations."""
    connection = sqlite3.connect(":memory:")
    connection.execute("CREATE TABLE users (id INTEGER, username TEXT)")
    connection.executemany(
        "INSERT INTO users VALUES (?, ?)",
        [(1, "alice"), (2, "bob")],
    )
    return connection


if __name__ == "__main__":
    demo_connection = create_demo_database()
    print(find_user(demo_connection, "alice"))
    print(render_greeting("visitor"))
