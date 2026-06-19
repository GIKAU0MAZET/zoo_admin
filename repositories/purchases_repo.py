from database import get_connection


def get_all_purchases():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            з.id_закупки,
            з.дата,
            з.id_заявки,

            п.наименование,
            к.название,
            сз.количество,
            сз.цена_за_кг

        FROM закупка з

        JOIN состав_закупки сз
            ON з.id_закупки = сз.id_закупки

        JOIN поставщик п
            ON сз.id_поставщика = п.id_поставщика

        JOIN корм к
            ON сз.id_корма = к.id_корма

        ORDER BY з.id_закупки DESC
    """)

    rows = cur.fetchall()

    conn.close()

    purchases = {}

    for row in rows:

        purchase_id = row[0]

        if purchase_id not in purchases:

            purchases[purchase_id] = {
                "id": row[0],
                "date": row[1],
                "request_id": row[2],
                "items": [],
                "total": 0
            }

        item_sum = float(row[5]) * float(row[6])

        purchases[purchase_id]["items"].append({
            "supplier": row[3],
            "food": row[4],
            "quantity": row[5],
            "price": row[6],
            "sum": item_sum
        })

        purchases[purchase_id]["total"] += item_sum

    return list(purchases.values())

def get_available_requests():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            з.id_заявки
        FROM заявки_на_закупку з
        WHERE з.статус_заявки = 'Одобрена'
        AND NOT EXISTS
        (
            SELECT 1
            FROM закупка п
            WHERE п.id_заявки = з.id_заявки
        )
        ORDER BY з.id_заявки
    """)

    rows = cur.fetchall()

    conn.close()

    return rows

def add_purchase(request_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO закупка
        (
            id_заявки,
            дата
        )
        VALUES
        (
            %s,
            CURRENT_DATE
        )
        RETURNING id_закупки
    """, (request_id,))

    purchase_id = cur.fetchone()[0]

    conn.commit()
    conn.close()

    return purchase_id