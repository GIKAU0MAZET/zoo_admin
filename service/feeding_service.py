from repositories.feeding_repo import get_all_feedings, add_feeding


def list_feedings():
    return get_all_feedings()


def create_feeding(animal_id, employee_id, feed, amount, note):
    add_feeding(animal_id, employee_id, feed, amount, note)