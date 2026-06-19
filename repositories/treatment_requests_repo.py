from database import get_connection


def get_all_treatment_requests():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            з."ID заявки",
            з.Дата,
            ж.кличка,
            с.фамилия || ' ' || с.имя || ' ' || с.отчество,
            з.Название,
            з.Статус
        FROM "Заявка на лечение" з

        JOIN животные ж
            ON з."ID животного"= ж.животное_id

        JOIN сотрудники с
            ON з."ID ветеринара" = с.сотрудник_id

        ORDER BY з."ID заявки" DESC
    """)

    rows = cur.fetchall()

    conn.close()

    return rows

def get_treatment_request_by_id(request_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            "ID заявки",
            Дата,
            "ID животного",
            "ID ветеринара",
            Название,
            Статус
        FROM "Заявка на лечение"
        WHERE "ID заявки" = %s
    """, (request_id,))

    row = cur.fetchone()

    conn.close()

    return row

def add_treatment_request(
        date,
        employee_id,
        animal_id,
        veterinarian_id,
        title,
        status,
        zoo_id
):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO "Заявка на лечение"
        (
            Дата,
            "ID сотрудника",
            "ID животного",
            "ID ветеринара",
            Название,
            Статус,
            "ID зоопарка"
        )
        VALUES
        (
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s
        )
    """, (
        date,
        employee_id,
        animal_id,
        veterinarian_id,
        title,
        status,
        zoo_id
    ))

    conn.commit()
    conn.close()
    
def update_treatment_request(
        request_id,
        animal_id,
        veterinarian_id,
        title,
        status
):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE "Заявка на лечение"
        SET
            "ID животного" = %s,
            "ID ветеринара" = %s,
            Название = %s,
            Статус = %s
        WHERE "ID заявки" = %s
    """, (
        animal_id,
        veterinarian_id,
        title,
        status,
        request_id
    ))

    conn.commit()
    conn.close()