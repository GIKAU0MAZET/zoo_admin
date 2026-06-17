from database import get_connection

def get_all_cages():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT вольер_id, номер FROM вольеры ORDER BY вольер_id")
    rows = cur.fetchall()

    conn.close()
    return rows