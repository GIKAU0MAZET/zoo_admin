from database import get_connection


def get_all_purchase_requests():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            z.id_заявки,
            z.дата,

            s1.фамилия || ' ' || s1.имя || ' ' || s1.отчество AS сотрудник,
            s2.фамилия || ' ' || s2.имя || ' ' || s2.отчество AS исполнитель,

            z.статус_заявки

        FROM заявки_на_закупку z

        JOIN сотрудники s1 ON s1.сотрудник_id = z.id_сотрудника
        JOIN сотрудники s2 ON s2.сотрудник_id = z.id_исполнителя

        ORDER BY z.id_заявки
    """)

    rows = cur.fetchall()

    conn.close()

    return rows

def get_purchase_request_by_id(request_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            id_заявки,
            дата,
            id_исполнителя,
            статус_заявки
        FROM заявки_на_закупку
        WHERE id_заявки = %s
    """, (request_id,))

    row = cur.fetchone()

    conn.close()

    return row

def add_purchase_request(
        date,
        employee_id,
        executor_id,
        status
):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO заявки_на_закупку
        (
            дата,
            id_сотрудника,
            id_исполнителя,
            статус_заявки
        )
        VALUES (%s, %s, %s, %s)
    """, (
        date,
        employee_id,
        executor_id,
        status
    ))

    conn.commit()
    conn.close()
    
def update_purchase_request(
        request_id,
        date,
        executor_id,
        status
):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE заявки_на_закупку
        SET
            дата = %s,
            id_исполнителя = %s,
            статус_заявки = %s
        WHERE id_заявки = %s
    """, (
        date,
        executor_id,
        status,
        request_id
    ))

    conn.commit()
    conn.close()
