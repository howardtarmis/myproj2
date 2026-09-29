"""Secure user lookup with parameterized SQL and output escaping."""

import html
import sqlite3


def find_user_secure(connection: sqlite3.Connection, username: str) -> dict | None:
    """Look up user by username using parameterized query.

    Args:
        connection: SQLite database connection
        username: Username to search for (untrusted input)

    Returns:
        User record as dict or None if not found
    """
    query = "SELECT id, username FROM users WHERE username = ?"
    cursor = connection.execute(query, (username,))
    row = cursor.fetchone()

    if row:
        return {"id": row[0], "username": row[1]}
    return None


def render_user_html(user: dict) -> str:
    """Render user info as HTML with output escaping.

    Args:
        user: User record dict

    Returns:
        HTML-escaped greeting
    """
    escaped_name = html.escape(user["username"])
    return f"<div class='user-greeting'><h1>Welcome, {escaped_name}!</h1></div>"


def create_demo_database() -> sqlite3.Connection:
    """Create a small in-memory database for local testing."""
    connection = sqlite3.connect(":memory:")
    connection.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT)")
    connection.executemany(
        "INSERT INTO users VALUES (?, ?)",
        [(1, "alice"), (2, "bob"), (3, "charlie")],
    )
    return connection


if __name__ == "__main__":
    db = create_demo_database()

    # Safe lookup
    user = find_user_secure(db, "alice")
    if user:
        print(render_user_html(user))

    # Attempt SQL injection (safely handled)
    user = find_user_secure(db, "' OR '1'='1")
    print(f"SQL injection attempt: {user}")  # Result: None (safe)
