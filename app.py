from flask import Flask, render_template, request, redirect, url_for
from service.animals_service import list_animals, create_animal, remove_animal
from repositories.dashboard_repo import get_dashboard_stats

app = Flask(__name__)

@app.route("/")
def dashboard():
    stats = get_dashboard_stats()
    return render_template("dashboard.html", **stats)

@app.route("/animals")
def animals():
    animals_list = list_animals()
    return render_template("animals.html", animals=animals_list)

@app.route("/animals/add", methods=["POST"])
def add_animal_route():
    name = request.form.get("name")
    age = request.form.get("age")

    create_animal(name, age)

    return redirect(url_for("animals"))

@app.route("/animals/delete/<int:animal_id>")
def delete_animal_route(animal_id):
    remove_animal(animal_id)
    return redirect(url_for("animals"))

if __name__ == "__main__":
    app.run(debug=True)