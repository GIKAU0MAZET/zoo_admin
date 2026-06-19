from database import get_connection


def get_all_veterinarians():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            сотрудник_id,
            фамилия,
            имя,
            отчество
        FROM сотрудники
        WHERE должность = 'Ветеринар'
        ORDER BY фамилия
    """)

    rows = cur.fetchall()

    conn.close()

    return rows