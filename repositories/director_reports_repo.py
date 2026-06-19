from database import get_connection


def get_animals_condition_report():
    """Состояние животных — последняя медзапись по каждому животному"""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT DISTINCT ON (ж.животное_id)
            ж.животное_id,
            ж.кличка,
            в.название AS вид,
            m."Состояние",
            m."Дата осмотра"
        FROM животные ж
        LEFT JOIN виды в ON в.вид_id = ж.вид_id
        LEFT JOIN "Медицинские записи" m ON m."ID животного" = ж.животное_id
        ORDER BY ж.животное_id, m."Дата осмотра" DESC NULLS LAST
    """)

    rows = cur.fetchall()
    conn.close()
    return rows


def get_medical_activity_report():
    """Мед. активность — количество осмотров по ветеринарам"""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            с.фамилия || ' ' || с.имя || ' ' || с.отчество AS ветеринар,
            COUNT(m."ID записи") AS количество_осмотров,
            MAX(m."Дата осмотра") AS последний_осмотр
        FROM сотрудники с
        LEFT JOIN "Медицинские записи" m ON m."ID сотрудника" = с.сотрудник_id
        WHERE с.должность = 'Ветеринар'
        GROUP BY с.сотрудник_id, с.фамилия, с.имя, с.отчество
        ORDER BY количество_осмотров DESC
    """)

    rows = cur.fetchall()
    conn.close()
    return rows


def get_finance_report():
    """Финансы — доходы от билетов и расходы на закупки"""
    conn = get_connection()
    cur = conn.cursor()

    # Доходы от билетов по месяцам
    cur.execute("""
        SELECT
            TO_CHAR("Дата", 'MM.YYYY') AS месяц,
            SUM("Цена" * "Количество") AS доход
        FROM "Билеты"
        GROUP BY TO_CHAR("Дата", 'MM.YYYY'), DATE_TRUNC('month', "Дата")
        ORDER BY DATE_TRUNC('month', "Дата") DESC
        LIMIT 12
    """)
    income = cur.fetchall()

    conn.close()
    return income


def get_attendance_report():
    """Посещаемость — количество билетов по типам и датам"""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            TO_CHAR("Дата", 'DD.MM.YYYY') AS дата,
            "Тип",
            SUM("Количество") AS посетители,
            SUM("Цена" * "Количество") AS выручка
        FROM "Билеты"
        GROUP BY DATE_TRUNC('day', "Дата"), TO_CHAR("Дата", 'DD.MM.YYYY'), "Тип"
        ORDER BY DATE_TRUNC('day', "Дата") DESC
        LIMIT 30
    """)

    rows = cur.fetchall()
    conn.close()
    return rows