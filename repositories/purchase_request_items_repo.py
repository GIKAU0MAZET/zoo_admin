from database import get_connection


def get_request_items(request_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            сз.id_заявки,
            п.наименование,
            к.название,
            сз.количество,
            сз.id_поставщика,
            сз.id_корма
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

def update_request_item(
        request_id,
        old_supplier_id,
        old_food_id,
        supplier_id,
        food_id,
        quantity
):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE состав_заявки
        SET
            id_поставщика = %s,
            id_корма = %s,
            количество = %s
        WHERE
            id_заявки = %s
            AND id_поставщика = %s
            AND id_корма = %s
    """, (
        supplier_id,
        food_id,
        quantity,
        request_id,
        old_supplier_id,
        old_food_id
    ))

    conn.commit()
    conn.close()
