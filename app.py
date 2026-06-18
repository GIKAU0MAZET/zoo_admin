from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from datetime import date

from repositories.dashboard_repo import get_dashboard_stats
from repositories.species_repo import get_all_species
from repositories.animals_repo import get_animal_by_id
from repositories.feed_repo import get_all_feed
from repositories.suppliers_repo import get_all_suppliers

from service.animals_service import list_animals, create_animal, remove_animal, edit_animal
from service.species_service import list_species
from service.cages_service import list_cages
from service.employees_service import list_employees
from service.auth_service import authenticate
from service.purchase_requests_service import list_purchase_requests, get_purchase_request, create_purchase_request, edit_purchase_request
from service.purchase_request_items_service import list_request_items, create_request_item, edit_request_item
from service.tickets_service import list_tickets, create_ticket

from database import get_connection


app = Flask(__name__)
app.secret_key = "zoo_secret_key_2026"

@app.context_processor
def inject_zoo_name():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""SELECT "Название зоопарка" FROM "Зоопарк" LIMIT 1""")
    row = cur.fetchone()
    conn.close()
    return {"zoo_name": row[0] if row else "Зоопарк"}

@app.route("/")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("login_page"))

    stats = get_dashboard_stats()

    return render_template(
        "dashboard.html",
        **stats
    )

# Авторизаиця
@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    login = request.form.get("login")
    password = request.form.get("password")

    user = authenticate(login, password)

    if not user:
        return render_template(
            "login.html",
            error="Неверный логин или пароль"
        )

    session["user_id"] = user[0]
    session["employee_id"] = user[3]
    session["role"] = user[4]        # ← добавить

    role = user[4]                   # ← добавить редирект по роли
    if role == "Кассир":
        return redirect(url_for("tickets"))
    else:
        return redirect(url_for("dashboard"))

#Выход
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

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

@app.route("/purchase-requests")
def purchase_requests():

    if "user_id" not in session:
        return redirect("/login")

    data = list_purchase_requests()

    return render_template(
        "purchase_requests.html",
        requests=data
    )
    
@app.route("/purchase-requests/<int:request_id>")
def purchase_request_items(request_id):

    request_info = get_purchase_request(request_id)

    items = list_request_items(request_id)

    suppliers = get_all_suppliers()

    feed = get_all_feed()

    return render_template(
        "purchase_request_items.html",
        request_info=request_info,
        request_id=request_id,
        items=items,
        suppliers=suppliers,
        feed=feed
    )
    
@app.route("/purchase-requests/add", methods=["POST"])
def add_purchase_request_route():

    employee_id = session.get("employee_id")

    if not employee_id:
        return redirect("/login")

    today = date.today()

    status = "Создана"

    executor_id = employee_id 

    create_purchase_request(
        today,
        employee_id,
        executor_id,
        status
    )

    return redirect("/purchase-requests")

@app.route(
    "/purchase-requests/<int:request_id>/add-item",
    methods=["POST"]
)
def add_purchase_request_item(request_id):

    supplier_id = request.form.get("supplier_id")
    food_id = request.form.get("food_id")
    quantity = request.form.get("quantity")

    create_request_item(
        request_id,
        supplier_id,
        food_id,
        quantity
    )

    if request.form.get("return_to") == "edit":
        return redirect(
            f"/purchase-requests/edit/{request_id}"
        )

    return redirect(
        f"/purchase-requests/{request_id}"
    )

@app.route("/purchase-requests/edit/<int:request_id>")
def edit_purchase_request_page(request_id):

    request_data = get_purchase_request(request_id)

    employees = list_employees()

    items = list_request_items(request_id)

    suppliers = get_all_suppliers()

    feed = get_all_feed()

    return render_template(
        "edit_purchase_request.html",
        request_data=request_data,
        request_id=request_id,
        employees=employees,
        items=items,
        suppliers=suppliers,
        feed=feed
    )
    
@app.route(
    "/purchase-requests/update/<int:request_id>",
    methods=["POST"]
)
def update_purchase_request_route(request_id):

    date = request.form.get("date")

    executor_id = request.form.get("executor_id")

    status = request.form.get("status")

    edit_purchase_request(
        request_id,
        date,
        executor_id,
        status
    )

    old_supplier_ids = request.form.getlist("old_supplier_id")
    old_food_ids = request.form.getlist("old_food_id")
    supplier_ids = request.form.getlist("supplier_id")
    food_ids = request.form.getlist("food_id")
    quantities = request.form.getlist("quantity")

    for old_supplier_id, old_food_id, supplier_id, food_id, quantity in zip(
            old_supplier_ids,
            old_food_ids,
            supplier_ids,
            food_ids,
            quantities
    ):
        edit_request_item(
            request_id,
            old_supplier_id,
            old_food_id,
            supplier_id,
            food_id,
            quantity
        )

    return redirect(
        f"/purchase-requests/edit/{request_id}"
    )
    
@app.route("/api/feed/<int:supplier_id>")
def get_feed_by_supplier(supplier_id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            id_корма,
            название
        FROM корм
        WHERE id_поставщика = %s
        ORDER BY название
    """, (supplier_id,))

    feed = cur.fetchall()

    conn.close()

    result = []

    for row in feed:
        result.append({
            "id": row[0],
            "name": row[1]
        })

    return jsonify(result)


#Кассир
@app.route("/tickets")
def tickets():
    if "user_id" not in session:
        return redirect("/login")
    if session.get("role") != "Кассир":   # ← добавить
        return redirect(url_for("dashboard"))

    data = list_tickets()
    return render_template("tickets.html", tickets=data)
 
 
@app.route("/tickets/add", methods=["POST"])
def add_ticket_route():
    if "user_id" not in session:
        return redirect("/login")
 
    ticket_type = request.form.get("ticket_type")
    quantity    = int(request.form.get("quantity", 1))
    employee_id = session.get("employee_id")
    zoo_id      = 1  
 
    create_ticket(ticket_type, quantity, employee_id, zoo_id)
 
    return redirect("/tickets")

if __name__ == "__main__":
    app.run(debug=True)
