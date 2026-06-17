from database import get_connection

def get_all_species():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT вид_id, название FROM виды ORDER BY вид_id")
    rows = cur.fetchall()

    conn.close()
    return rows