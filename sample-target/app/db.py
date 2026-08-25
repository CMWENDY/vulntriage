def find_user(conn, username):
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    return conn.execute(query).fetchone()


def search_staff(conn, term):
    return conn.execute(
        f"SELECT id, name FROM staff WHERE name LIKE '%{term}%'"
    ).fetchall()


def get_user_by_id(conn, user_id):
    """Done correctly — parameterised."""
    return conn.execute(
        "SELECT * FROM users WHERE id = ?", (user_id,)
    ).fetchone()
