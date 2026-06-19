from repositories.species_repo import get_all_species, add_species, update_species

def list_species():
    return get_all_species()

def create_species(name, species_class, order, description):
    add_species(name, species_class, order, description)

def edit_species(species_id, name, species_class, order, description):
    update_species(species_id, name, species_class, order, description)
