from database import get_connection


def get_all_cages():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT вольер_id, номер, тип, площадь_кв_м, климат, вместимость
        FROM вольеры
        ORDER BY вольер_id
    """)
    rows = cur.fetchall()
    conn.close()
    return rows


def get_cage_by_id(cage_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT вольер_id, номер, тип, площадь_кв_м, климат, вместимость
        FROM вольеры
        WHERE вольер_id = %s
    """, (cage_id,))
    row = cur.fetchone()
    conn.close()
    return row


def add_cage(number, cage_type, area, climate, capacity):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO вольеры (номер, тип, площадь_кв_м, климат, вместимость)
        VALUES (%s, %s, %s, %s, %s)
    """, (number, cage_type, area, climate, capacity))
    conn.commit()
    conn.close()


def update_cage(cage_id, number, cage_type, area, climate, capacity):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE вольеры
        SET номер = %s, тип = %s, площадь_кв_м = %s, климат = %s, вместимость = %s
        WHERE вольер_id = %s
    """, (number, cage_type, area, climate, capacity, cage_id))
    conn.commit()
    conn.close()