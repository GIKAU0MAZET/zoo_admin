from database import get_connection


def get_all_medical_records():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            m."ID записи",
            m."ID заявки",
            a.кличка AS животное,
            s.фамилия || ' ' || s.имя || ' ' || s.отчество AS ветеринар,
            m."Название",
            m."Дата осмотра",
            m."Состояние"
        FROM "Медицинские записи" m
        JOIN животные a ON a.животное_id = m."ID животного"
        JOIN сотрудники s ON s.сотрудник_id = m."ID сотрудника"
        ORDER BY m."Дата осмотра" DESC
    """)

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