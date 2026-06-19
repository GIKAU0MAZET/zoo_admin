from repositories.cages_repo import get_all_cages
from repositories.cages_repo import get_all_cages, add_cage, update_cage

def list_cages():
    return get_all_cages()

def create_cage(number, cage_type, area, climate, capacity):
    add_cage(number, cage_type, area, climate, capacity)

def edit_cage(cage_id, number, cage_type, area, climate, capacity):
    update_cage(cage_id, number, cage_type, area, climate, capacity)