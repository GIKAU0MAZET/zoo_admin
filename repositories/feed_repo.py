from database import get_connection


def get_all_feed():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            id_корма,
            название
        FROM корм
        ORDER BY название
    """)

    rows = cur.fetchall()

    conn.close()

    return rows