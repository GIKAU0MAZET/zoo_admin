from flask import Flask, render_template, request, redirect, url_for
from service.animals_service import list_animals, create_animal, remove_animal, edit_animal
from repositories.dashboard_repo import get_dashboard_stats
from repositories.species_repo import get_all_species
from repositories.animals_repo import get_animal_by_id
from service.species_service import list_species
from service.cages_service import list_cages
from service.employees_service import list_employees


app = Flask(__name__)

@app.route("/")
def dashboard():
    stats = get_dashboard_stats()
    return render_template("dashboard.html", **stats)

@app.route("/animals")
def animals():
    animals_list = list_animals()
    species = get_all_species()

    return render_template(
        "animals.html",
        animals=animals_list,
        species=species
    )

@app.route("/animals/add", methods=["POST"])
def add_animal_route():
    name = request.form.get("name")
    birth_date = request.form.get("birth_date")
    species_id = request.form.get("species_id")

    create_animal(name, birth_date, species_id)

    return redirect(url_for("animals"))

@app.route("/animals/delete/<int:animal_id>")
def delete_animal_route(animal_id):
    remove_animal(animal_id)
    return redirect(url_for("animals"))

@app.route("/animals/edit/<int:animal_id>")
def edit_animal_page(animal_id):
    animal = get_animal_by_id(animal_id)

    return render_template(
        "edit_animal.html",
        animal=animal
    )

@app.route("/animals/update/<int:animal_id>", methods=["POST"])
def update_animal_route(animal_id):
    name = request.form.get("name")
    birth_date = request.form.get("birth_date")

    edit_animal(animal_id, name, birth_date)

    return redirect(url_for("animals"))

@app.route("/species")
def species():
    data = list_species()
    return render_template("species.html", species=data)

@app.route("/cages")
def cages():
    data = list_cages()
    return render_template("cages.html", cages=data)

@app.route("/employees")
def employees():
    data = list_employees()
    return render_template("employees.html", employees=data)

if __name__ == "__main__":
    app.run(debug=True)