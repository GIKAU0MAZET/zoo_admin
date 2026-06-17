from database import get_connection

def get_all_animals():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            животные.животное_id,
            животные.кличка,
            животные.дата_рождения,
            виды.название
        FROM животные
        LEFT JOIN виды ON животные.вид_id = виды.вид_id
        ORDER BY животные.животное_id
    """)
    rows = cur.fetchall()

    conn.close()
    return rows

def get_animal_by_id(animal_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            животное_id,
            кличка,
            дата_рождения,
            вид_id
        FROM животные
        WHERE животное_id = %s
    """, (animal_id,))

    animal = cur.fetchone()

    conn.close()

    return animal


def add_animal(name, birth_date, species_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO животные (кличка, дата_рождения, вид_id)
        VALUES (%s, %s, %s)
    """, (name, birth_date, species_id))

    conn.commit()
    conn.close()


def delete_animal(animal_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM животные WHERE животное_id = %s",
        (animal_id,)
    )

    conn.commit()
    conn.close()
    
def update_animal(animal_id, name, birth_date):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "UPDATE животные SET кличка = %s, дата_рождения = %s WHERE животное_id = %s",
        (name, birth_date, animal_id)
    )

    conn.commit()
    conn.close()
    
    
    