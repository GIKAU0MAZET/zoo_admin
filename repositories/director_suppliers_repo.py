from database import get_connection


def get_all_suppliers_full():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            id_поставщика,
            наименование,
            юридический_адрес,
            фактический_адрес,
            телефон,
            электронная_почта
        FROM поставщик
        ORDER BY наименование
    """)

    rows = cur.fetchall()
    conn.close()
    return rows


def get_supplier_by_id(supplier_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            id_поставщика,
            наименование,
            юридический_адрес,
            фактический_адрес,
            телефон,
            электронная_почта
        FROM поставщик
        WHERE id_поставщика = %s
    """, (supplier_id,))

    row = cur.fetchone()
    conn.close()
    return row


def add_supplier(name, legal_address, actual_address, phone, email):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO поставщик
            (наименование, юридический_адрес, фактический_адрес, телефон, электронная_почта)
        VALUES (%s, %s, %s, %s, %s)
    """, (name, legal_address, actual_address, phone, email))

    conn.commit()
    conn.close()


def update_supplier(supplier_id, name, legal_address, actual_address, phone, email):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE поставщик
        SET
            наименование = %s,
            юридический_адрес = %s,
            фактический_адрес = %s,
            телефон = %s,
            электронная_почта = %s
        WHERE id_поставщика = %s
    """, (name, legal_address, actual_address, phone, email, supplier_id))

    conn.commit()
    conn.close()