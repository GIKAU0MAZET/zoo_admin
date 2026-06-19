from database import get_connection


def get_all_species():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT вид_id, название, класс, отряд, описание
        FROM виды
        ORDER BY вид_id
    """)
    rows = cur.fetchall()
    conn.close()
    return rows


def get_species_by_id(species_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT вид_id, название, класс, отряд, описание
        FROM виды
        WHERE вид_id = %s
    """, (species_id,))
    row = cur.fetchone()
    conn.close()
    return row


def add_species(name, species_class, order, description):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO виды (название, класс, отряд, описание)
        VALUES (%s, %s, %s, %s)
    """, (name, species_class, order, description))
    conn.commit()
    conn.close()


def update_species(species_id, name, species_class, order, description):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE виды
        SET название = %s, класс = %s, отряд = %s, описание = %s
        WHERE вид_id = %s
    """, (name, species_class, order, description, species_id))
    conn.commit()
    conn.close()