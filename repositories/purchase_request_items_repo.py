from database import get_connection


def get_request_items(request_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            сз.id_заявки,
            п.наименование,
            к.название,
            сз.количество
        FROM состав_заявки сз
        JOIN поставщик п
            ON сз.id_поставщика = п.id_поставщика
        JOIN корм к
            ON сз.id_корма = к.id_корма
        WHERE сз.id_заявки = %s
    """, (request_id,))

    rows = cur.fetchall()

    conn.close()

    return rows

def add_request_item(
        request_id,
        supplier_id,
        food_id,
        quantity
):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO состав_заявки
        (
            id_заявки,
            id_поставщика,
            id_корма,
            количество
        )
        VALUES (%s, %s, %s, %s)
    """, (
        request_id,
        supplier_id,
        food_id,
        quantity
    ))

    conn.commit()
    conn.close()