"""Secure user lookup and HTML rendering example."""

import html
import sqlite3


def render_user(connection: sqlite3.Connection, username: str) -> str:
    """Look up a user safely and render the result as escaped HTML."""
    row = connection.execute(
        "SELECT id, username FROM users WHERE username = ?",
        (username,),
    ).fetchone()
    if row is None:
        return "<p>User not found.</p>"

    user_id, stored_username = row
    safe_username = html.escape(str(stored_username), quote=True)
    return f"<p>User {user_id}: {safe_username}</p>"


def create_demo_database() -> sqlite3.Connection:
    """Create a small in-memory database for the example."""
    connection = sqlite3.connect(":memory:")
    connection.execute("CREATE TABLE users (id INTEGER, username TEXT)")
    connection.execute("INSERT INTO users VALUES (?, ?)", (1, "alice"))
    return connection


if __name__ == "__main__":
    demo_connection = create_demo_database()
    print(render_user(demo_connection, "alice"))
    print(render_user(demo_connection, "<script>alert(1)</script>"))
