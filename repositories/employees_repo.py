from database import get_connection

def get_all_employees():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT сотрудник_id, имя FROM сотрудники ORDER BY сотрудник_id")
    rows = cur.fetchall()

    conn.close()
    return rows