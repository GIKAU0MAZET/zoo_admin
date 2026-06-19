from database import get_connection


def get_all_employees_full():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            сотрудник_id,
            фамилия,
            имя,
            отчество,
            должность,
            телефон,
            дата_приема
        FROM сотрудники
        ORDER BY фамилия
    """)

    rows = cur.fetchall()
    conn.close()
    return rows


def get_employee_by_id(employee_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            сотрудник_id,
            фамилия,
            имя,
            отчество,
            должность,
            телефон,
            дата_приема
        FROM сотрудники
        WHERE сотрудник_id = %s
    """, (employee_id,))

    row = cur.fetchone()
    conn.close()
    return row


def add_employee(last_name, first_name, middle_name, position, phone, hire_date, zoo_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO сотрудники
            (фамилия, имя, отчество, должность, телефон, дата_приема, "ID зоопарка")
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (last_name, first_name, middle_name, position, phone, hire_date, zoo_id))

    conn.commit()
    conn.close()


def update_employee(employee_id, last_name, first_name, middle_name, position, phone, hire_date):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE сотрудники
        SET
            фамилия = %s,
            имя = %s,
            отчество = %s,
            должность = %s,
            телефон = %s,
            дата_приема = %s
        WHERE сотрудник_id = %s
    """, (last_name, first_name, middle_name, position, phone, hire_date, employee_id))

    conn.commit()
    conn.close()