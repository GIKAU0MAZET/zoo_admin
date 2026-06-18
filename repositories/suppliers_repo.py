from database import get_connection


def get_all_suppliers():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            id_поставщика,
            наименование
        FROM поставщик
        ORDER BY наименование
    """)

    rows = cur.fetchall()

    conn.close()

    return rows