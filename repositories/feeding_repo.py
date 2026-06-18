from database import get_connection


def get_all_feedings():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            k.кормление_id,
            a.кличка AS животное,
            s.фамилия || ' ' || s.имя || ' ' || s.отчество AS смотритель,
            k.дата_время,
            k.корм,
            k.количество_г,
            k.примечание
        FROM кормление k
        JOIN животные a ON a.животное_id = k.животное_id
        JOIN сотрудники s ON s.сотрудник_id = k.сотрудник_id
        ORDER BY k.дата_время DESC
    """)

    rows = cur.fetchall()
    conn.close()
    return rows


def add_feeding(animal_id, employee_id, feed, amount, note):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO кормление
            (животное_id, сотрудник_id, дата_время, корм, количество_г, примечание)
        VALUES (%s, %s, NOW(), %s, %s, %s)
    """, (animal_id, employee_id, feed, amount, note))

    conn.commit()
    conn.close()