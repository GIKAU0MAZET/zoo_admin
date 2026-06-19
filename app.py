from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from datetime import date

from repositories.dashboard_repo import get_dashboard_stats
from repositories.species_repo import get_all_species
from repositories.animals_repo import get_animal_by_id, get_animals_for_select
from repositories.feed_repo import get_all_feed
from repositories.suppliers_repo import get_all_suppliers
from repositories.veterinarians_repo import get_all_veterinarians
from repositories.purchases_repo import get_available_requests

from service.animals_service import list_animals, create_animal, remove_animal, edit_animal
from service.species_service import list_species
from service.cages_service import list_cages
from service.employees_service import list_employees
from service.auth_service import authenticate
from service.purchase_requests_service import list_purchase_requests, get_purchase_request, create_purchase_request, edit_purchase_request
from service.purchase_request_items_service import list_request_items, create_request_item, edit_request_item
from service.tickets_service import list_tickets, create_ticket
from service.feeding_service import list_feedings, create_feeding
from service.medical_records_service import list_treatment_requests_for_vet, list_medical_records_for_vet, create_medical_record, get_request_for_vet
from service.treatment_requests_service import list_treatment_requests, create_treatment_request, get_treatment_request, edit_treatment_request
from service.purchases_service import list_purchases, create_purchase
from service.director_service import (
    list_employees_full, get_employee, create_employee, edit_employee,
    list_suppliers_full, get_supplier, create_supplier, edit_supplier,
    report_animals_condition, report_medical_activity,
    report_finance, report_attendance
)
from repositories.cages_repo import get_cage_by_id
from repositories.species_repo import get_species_by_id
from service.cages_service import list_cages, create_cage, edit_cage
from service.species_service import list_species, create_species, edit_species

from database import get_connection


app = Flask(__name__)
app.secret_key = "zoo_secret_key_2026"

@app.context_processor
def inject_current_user():
    if "employee_id" not in session:
        return {"current_user": None}
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT фамилия || ' ' || имя || ' ' || отчество
        FROM сотрудники
        WHERE сотрудник_id = %s
    """, (session["employee_id"],))
    row = cur.fetchone()
    conn.close()
    return {"current_user": row[0] if row else None}

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
    session["role"] = user[4]        

    role = user[4]
    if role == "Кассир":
        return redirect(url_for("tickets"))
    elif role == "Смотритель":
        return redirect(url_for("watcher_animals"))
    elif role == "Ветеринар":
        return redirect(url_for("vet_animals"))
    elif role == "Директор":
        return redirect(url_for("director_employees"))
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

# ── ВИДЫ ─────────────────────────────────────────────────────
 
@app.route("/species")
def species():
    data = list_species()
    return render_template("species.html", species=data)
 
 
@app.route("/species/add", methods=["POST"])
def add_species_route():
    create_species(
        request.form.get("name"),
        request.form.get("species_class"),
        request.form.get("order"),
        request.form.get("description"),
    )
    return redirect("/species")
 
 
@app.route("/species/edit/<int:species_id>", methods=["GET", "POST"])
def edit_species_page(species_id):
    if request.method == "POST":
        edit_species(
            species_id,
            request.form.get("name"),
            request.form.get("species_class"),
            request.form.get("order"),
            request.form.get("description"),
        )
        return redirect("/species")
 
    s = get_species_by_id(species_id)
    return render_template("edit_species.html", species=s)

# ── ВОЛЬЕРЫ ──────────────────────────────────────────────────
 
@app.route("/cages")
def cages():
    data = list_cages()
    return render_template("cages.html", cages=data)
 
 
@app.route("/cages/add", methods=["POST"])
def add_cage_route():
    create_cage(
        request.form.get("number"),
        request.form.get("cage_type"),
        request.form.get("area") or None,
        request.form.get("climate"),
        request.form.get("capacity") or None,
    )
    return redirect("/cages")
 
 
@app.route("/cages/edit/<int:cage_id>", methods=["GET", "POST"])
def edit_cage_page(cage_id):
    if request.method == "POST":
        edit_cage(
            cage_id,
            request.form.get("number"),
            request.form.get("cage_type"),
            request.form.get("area") or None,
            request.form.get("climate"),
            request.form.get("capacity") or None,
        )
        return redirect("/cages")
 
    cage = get_cage_by_id(cage_id)
    return render_template("edit_cage.html", cage=cage)

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

@app.route("/treatment-requests")
def treatment_requests():

    requests = list_treatment_requests()

    animals = get_animals_for_select()

    veterinarians = get_all_veterinarians()

    return render_template(
        "treatment_requests.html",
        requests=requests,
        animals=animals,
        veterinarians=veterinarians
    )

@app.route(
    "/treatment-requests/add",
    methods=["POST"]
)
def add_treatment_request_route():

    animal_id = request.form.get("animal_id")

    veterinarian_id = request.form.get("veterinarian_id")

    title = request.form.get("title")

    status = request.form.get("status")

    employee_id = session["employee_id"]

    zoo_id = 1

    create_treatment_request(
        employee_id,
        animal_id,
        veterinarian_id,
        title,
        status,
        zoo_id
    )

    return redirect("/treatment-requests")

@app.route("/treatment-requests/edit/<int:request_id>")
def edit_treatment_request_page(request_id):
    request_data = get_treatment_request(request_id)

    if request_data and request_data[5] == "Завершена":  # ← добавить
        return redirect("/treatment-requests")

    animals = get_animals_for_select()
    veterinarians = get_all_veterinarians()

    return render_template(
        "edit_treatment_request.html",
        request_data=request_data,
        animals=animals,
        veterinarians=veterinarians
    )
    
@app.route(
    "/treatment-requests/update/<int:request_id>",
    methods=["POST"]
)
def update_treatment_request_route(request_id):

    animal_id = request.form.get("animal_id")

    veterinarian_id = request.form.get("veterinarian_id")

    title = request.form.get("title")

    status = request.form.get("status")

    edit_treatment_request(
        request_id,
        animal_id,
        veterinarian_id,
        title,
        status
    )

    return redirect("/treatment-requests")  

@app.route("/purchases")
def purchases():

    purchases_data = list_purchases()

    available_requests = get_available_requests()

    return render_template(
        "purchases.html",
        purchases=purchases_data,
        requests=available_requests
    )
    
@app.route(
    "/purchases/add",
    methods=["POST"]
)
def add_purchase_route():

    request_id = request.form.get("request_id")

    create_purchase(request_id)

    return redirect("/purchases")   

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


#Смотритель
@app.route("/watcher/animals")
def watcher_animals():
    if "user_id" not in session:
        return redirect("/login")
    if session.get("role") != "Смотритель":
        return redirect(url_for("dashboard"))
 
    animals_list = list_animals()
    print(">>> animals_list:", animals_list)
    return render_template("watcher_animals.html", animals=animals_list)
 
 
# Смотритель — кормление
@app.route("/feeding")
def feeding():
    if "user_id" not in session:
        return redirect("/login")
    if session.get("role") != "Смотритель":
        return redirect(url_for("dashboard"))
 
    data = list_feedings()
    animals_list = list_animals()
    return render_template("feeding.html", feedings=data, animals=animals_list)
 
 
@app.route("/feeding/add", methods=["POST"])
def add_feeding_route():
    if "user_id" not in session:
        return redirect("/login")
    if session.get("role") != "Смотритель":
        return redirect(url_for("dashboard"))
 
    animal_id   = request.form.get("animal_id")
    employee_id = session.get("employee_id")
    feed        = request.form.get("feed")
    amount      = request.form.get("amount")
    note        = request.form.get("note", "")
 
    create_feeding(animal_id, employee_id, feed, amount, note)
    return redirect("/feeding")

#Ветеринар
@app.route("/vet/animals")
def vet_animals():
    if "user_id" not in session:
        return redirect("/login")
    if session.get("role") != "Ветеринар":
        return redirect(url_for("dashboard"))
 
    animals_list = list_animals()
    return render_template("vet_animals.html", animals=animals_list)
 
 
# Ветеринар — список заявок на лечение + медзаписи
@app.route("/medical-records")
def medical_records():
    if "user_id" not in session:
        return redirect("/login")
    if session.get("role") != "Ветеринар":
        return redirect(url_for("dashboard"))
 
    employee_id = session.get("employee_id")
    treatment_requests = list_treatment_requests_for_vet(employee_id)
    records = list_medical_records_for_vet(employee_id)
 
    return render_template(
        "medical_records.html",
        treatment_requests=treatment_requests,
        records=records
    )
 
 
# Ветеринар — форма создания медзаписи по конкретной заявке
@app.route("/medical-records/add/<int:request_id>")
def add_medical_record_page(request_id):
    if "user_id" not in session:
        return redirect("/login")
    if session.get("role") != "Ветеринар":
        return redirect(url_for("dashboard"))
 
    employee_id = session.get("employee_id")
    treatment_request = get_request_for_vet(request_id, employee_id)
 
    if not treatment_request:
        return redirect("/medical-records")
 
    return render_template(
        "add_medical_record.html",
        treatment_request=treatment_request
    )
 
 
@app.route("/medical-records/add/<int:request_id>", methods=["POST"])
def add_medical_record_route(request_id):
    if "user_id" not in session:
        return redirect("/login")
    if session.get("role") != "Ветеринар":
        return redirect(url_for("dashboard"))
 
    employee_id = session.get("employee_id")
    treatment_request = get_request_for_vet(request_id, employee_id)
 
    if not treatment_request:
        return redirect("/medical-records")
 
    animal_id = treatment_request[2]  # ID животного из заявки
    name      = request.form.get("name")
    date      = request.form.get("date")
    condition = request.form.get("condition")
 
    create_medical_record(request_id, animal_id, employee_id, name, date, condition)
    return redirect("/medical-records")

#Директор
# ── ПЕРСОНАЛ ──────────────────────────────────────────────────
 
@app.route("/director/employees")
def director_employees():
    if "user_id" not in session or session.get("role") != "Директор":
        return redirect("/login")
    data = list_employees_full()
    return render_template("director_employees.html", employees=data)
 
 
@app.route("/director/employees/add", methods=["GET", "POST"])
def director_add_employee():
    if "user_id" not in session or session.get("role") != "Директор":
        return redirect("/login")
 
    if request.method == "POST":
        create_employee(
            request.form.get("last_name"),
            request.form.get("first_name"),
            request.form.get("middle_name"),
            request.form.get("position"),
            request.form.get("phone"),
            request.form.get("hire_date"),
        )
        return redirect("/director/employees")
 
    return render_template("director_employee_form.html", employee=None)
 
 
@app.route("/director/employees/edit/<int:employee_id>", methods=["GET", "POST"])
def director_edit_employee(employee_id):
    if "user_id" not in session or session.get("role") != "Директор":
        return redirect("/login")
 
    if request.method == "POST":
        edit_employee(
            employee_id,
            request.form.get("last_name"),
            request.form.get("first_name"),
            request.form.get("middle_name"),
            request.form.get("position"),
            request.form.get("phone"),
            request.form.get("hire_date"),
        )
        return redirect("/director/employees")
 
    employee = get_employee(employee_id)
    return render_template("director_employee_form.html", employee=employee)
 
 
# ── ПОСТАВЩИКИ ────────────────────────────────────────────────
 
@app.route("/director/suppliers")
def director_suppliers():
    if "user_id" not in session or session.get("role") != "Директор":
        return redirect("/login")
    data = list_suppliers_full()
    return render_template("director_suppliers.html", suppliers=data)
 
 
@app.route("/director/suppliers/add", methods=["GET", "POST"])
def director_add_supplier():
    if "user_id" not in session or session.get("role") != "Директор":
        return redirect("/login")
 
    if request.method == "POST":
        create_supplier(
            request.form.get("name"),
            request.form.get("legal_address"),
            request.form.get("actual_address"),
            request.form.get("phone"),
            request.form.get("email"),
        )
        return redirect("/director/suppliers")
 
    return render_template("director_supplier_form.html", supplier=None)
 
 
@app.route("/director/suppliers/edit/<int:supplier_id>", methods=["GET", "POST"])
def director_edit_supplier(supplier_id):
    if "user_id" not in session or session.get("role") != "Директор":
        return redirect("/login")
 
    if request.method == "POST":
        edit_supplier(
            supplier_id,
            request.form.get("name"),
            request.form.get("legal_address"),
            request.form.get("actual_address"),
            request.form.get("phone"),
            request.form.get("email"),
        )
        return redirect("/director/suppliers")
 
    supplier = get_supplier(supplier_id)
    return render_template("director_supplier_form.html", supplier=supplier)
 
 
# ── ЗАЯВКИ (только просмотр) ──────────────────────────────────
 
@app.route("/director/purchase-requests")
def director_purchase_requests():
    if "user_id" not in session or session.get("role") != "Директор":
        return redirect("/login")
    data = list_purchase_requests()
    return render_template("director_purchase_requests.html", requests=data)
 
 
@app.route("/director/treatment-requests")
def director_treatment_requests():
    if "user_id" not in session or session.get("role") != "Директор":
        return redirect("/login")
    data = list_treatment_requests()
    return render_template("director_treatment_requests.html", requests=data)
 
 
# ── ОТЧЁТЫ ────────────────────────────────────────────────────
 
@app.route("/director/reports")
def director_reports():
    if "user_id" not in session or session.get("role") != "Директор":
        return redirect("/login")
 
    return render_template("director_reports.html")
 
 
@app.route("/director/reports/animals")
def director_report_animals():
    if "user_id" not in session or session.get("role") != "Директор":
        return redirect("/login")
    data = report_animals_condition()
    return render_template("director_report_animals.html", animals=data)
 
 
@app.route("/director/reports/medical")
def director_report_medical():
    if "user_id" not in session or session.get("role") != "Директор":
        return redirect("/login")
    data = report_medical_activity()
    return render_template("director_report_medical.html", vets=data)
 
 
@app.route("/director/reports/finance")
def director_report_finance():
    if "user_id" not in session or session.get("role") != "Директор":
        return redirect("/login")
    data = report_finance()
    return render_template("director_report_finance.html", income=data)
 
 
@app.route("/director/reports/attendance")
def director_report_attendance():
    if "user_id" not in session or session.get("role") != "Директор":
        return redirect("/login")
    data = report_attendance()
    return render_template("director_report_attendance.html", rows=data)

if __name__ == "__main__":
    app.run(debug=True)
