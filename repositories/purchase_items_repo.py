from database import get_connection


def copy_request_items_to_purchase(
        request_id,
        purchase_id
):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO состав_закупки
        (
            id_закупки,
            id_поставщика,
            id_корма,
            количество,
            цена_за_кг
        )
        SELECT
            %s,
            id_поставщика,
            id_корма,
            количество,
            0
        FROM состав_заявки
        WHERE id_заявки = %s
    """, (
        purchase_id,
        request_id
    ))

    conn.commit()
    conn.close()
    
def get_purchase_items(purchase_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            с.id,
            п.наименование,
            к.название,
            с.количество,
            с.цена_за_кг
        FROM состав_закупки с

        JOIN поставщики п
            ON с.id_поставщика = п.id_поставщика

        JOIN корм к
            ON с.id_корма = к.id_корма

        WHERE с.id_закупки = %s
    """, (purchase_id,))

    rows = cur.fetchall()

    conn.close()

    return rows