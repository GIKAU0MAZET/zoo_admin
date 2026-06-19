from database import get_connection


def get_treatment_requests_for_vet(employee_id):
    """Заявки на лечение назначенные конкретному ветеринару"""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            з."ID заявки",
            з."Дата",
            ж.кличка,
            з."Название",
            з."Статус"
        FROM "Заявка на лечение" з
        JOIN животные ж ON з."ID животного" = ж.животное_id
        WHERE з."ID ветеринара" = %s
        ORDER BY з."ID заявки" DESC
    """, (employee_id,))

    rows = cur.fetchall()
    conn.close()
    return rows


def get_medical_records_for_vet(employee_id):
    """Медзаписи созданные конкретным ветеринаром"""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            m."ID записи",
            ж.кличка AS животное,
            м_с.фамилия || ' ' || м_с.имя || ' ' || м_с.отчество AS ветеринар,
            m."Название",
            m."Дата осмотра",
            m."Состояние",
            m."ID заявки"
        FROM "Медицинские записи" m
        JOIN животные ж ON ж.животное_id = m."ID животного"
        JOIN сотрудники м_с ON м_с.сотрудник_id = m."ID сотрудника"
        WHERE m."ID сотрудника" = %s
        ORDER BY m."Дата осмотра" DESC
    """, (employee_id,))

    rows = cur.fetchall()
    conn.close()
    return rows


def add_medical_record(request_id, animal_id, employee_id, name, date, condition):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO "Медицинские записи"
            ("ID заявки", "ID животного", "ID сотрудника", "Название", "Дата осмотра", "Состояние")
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (request_id, animal_id, employee_id, name, date, condition))

    conn.commit()
    conn.close()


def update_treatment_request_status(request_id, status):
    """Обновить статус заявки после создания медзаписи"""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE "Заявка на лечение"
        SET "Статус" = %s
        WHERE "ID заявки" = %s
    """, (status, request_id))

    conn.commit()
    conn.close()


def get_treatment_request_for_vet(request_id, employee_id):
    """Получить заявку по ID — только если она назначена этому ветеринару"""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            з."ID заявки",
            з."Дата",
            з."ID животного",
            ж.кличка,
            з."Название",
            з."Статус"
        FROM "Заявка на лечение" з
        JOIN животные ж ON з."ID животного" = ж.животное_id
        WHERE з."ID заявки" = %s
          AND з."ID ветеринара" = %s
    """, (request_id, employee_id))

    row = cur.fetchone()
    conn.close()
    return row