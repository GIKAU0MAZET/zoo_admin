from database import get_connection

def get_dashboard_stats():
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT
                (SELECT COUNT(*) FROM животные),
                (SELECT COUNT(*) FROM виды),
                (SELECT COUNT(*) FROM вольеры),
                (SELECT COUNT(*) FROM сотрудники)
        """)

        return dict(zip(
            ["animals_count", "species_count", "cages_count", "employees_count"],
            cur.fetchone()
        ))

    finally:
        conn.close()