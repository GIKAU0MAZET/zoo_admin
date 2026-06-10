from database import get_connection

def get_all_animals():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT животное_id, кличка, дата_рождения FROM животные ORDER BY животное_id")
    rows = cur.fetchall()

    conn.close()
    return rows


def add_animal(name, age):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO животные (name, age) VALUES (%s, %s)",
        (name, age)
    )

    conn.commit()
    conn.close()


def delete_animal(animal_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM животные WHERE id = %s",
        (animal_id,)
    )

    conn.commit()
    conn.close()