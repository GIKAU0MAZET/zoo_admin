from repositories.animals_repo import (
    get_all_animals,
    add_animal,
    delete_animal
)

def list_animals():
    return get_all_animals()

def create_animal(name, age):
    add_animal(name, age)

def remove_animal(animal_id):
    delete_animal(animal_id)