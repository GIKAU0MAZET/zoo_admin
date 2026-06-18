from database import get_connection


def get_user_by_login(login):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            п.пользователь_id,
            п.логин,
            п.пароль_hash,
            с.сотрудник_id
        FROM пользователи п
        JOIN сотрудники с
            ON п.сотрудник_id = с.сотрудник_id
        WHERE п.логин = %s
    """, (login,))

    user = cur.fetchone()

    conn.close()

    return user