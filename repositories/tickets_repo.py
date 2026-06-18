from database import get_connection


def get_all_tickets():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            b."ID билета",
            b.Дата,
            b.Тип,
            b.Цена,
            b.Количество,
            b.Цена * b.Количество AS сумма,
            s.фамилия || ' ' || s.имя || ' ' || s.отчество AS кассир
        FROM Билеты b
        JOIN сотрудники s ON s.сотрудник_id = b."ID сотрудника"
        ORDER BY b."ID билета" DESC
    """)

    rows = cur.fetchall()
    conn.close()
    return rows


def add_ticket(date, ticket_type, price, quantity, employee_id, zoo_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO Билеты
            (Дата, Тип, Цена, Количество, "ID сотрудника", "ID зоопарка")
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (date, ticket_type, price, quantity, employee_id, zoo_id))

    conn.commit()
    conn.close()