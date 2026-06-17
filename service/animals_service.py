from repositories.animals_repo import get_all_animals, add_animal, delete_animal, update_animal
from datetime import date

def create_animal(name, birth_date):
    add_animal(name, birth_date)

def remove_animal(animal_id):
    delete_animal(animal_id)

def edit_animal(animal_id, name, birth_date):
    update_animal(animal_id, name, birth_date)

# Вычисление возраста
def calculate_age(birth_date):
    today = date.today()
    return today.year - birth_date.year - (
        (today.month, today.day) < (birth_date.month, birth_date.day)
    )


def list_animals():
    animals = get_all_animals()

    result = []
    for a in animals:
        animal_id = a[0]
        name = a[1]
        birth_date = a[2]
        species = a[3]

        age = calculate_age(birth_date)   # 👈 ВОТ ЭТОГО НЕ ХВАТАЛО

        result.append({
            "id": animal_id,
            "name": name,
            "birth_date": birth_date,
            "species": species,
            "age": age
        })

    return result