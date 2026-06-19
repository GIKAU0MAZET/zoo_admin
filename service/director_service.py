from repositories.director_employees_repo import (
    get_all_employees_full, get_employee_by_id,
    add_employee, update_employee
)
from repositories.director_suppliers_repo import (
    get_all_suppliers_full, get_supplier_by_id,
    add_supplier, update_supplier
)
from repositories.director_reports_repo import (
    get_animals_condition_report,
    get_medical_activity_report,
    get_finance_report,
    get_attendance_report
)


# Сотрудники
def list_employees_full():
    return get_all_employees_full()

def get_employee(employee_id):
    return get_employee_by_id(employee_id)

def create_employee(last_name, first_name, middle_name, position, phone, hire_date, zoo_id=1):
    add_employee(last_name, first_name, middle_name, position, phone, hire_date, zoo_id)

def edit_employee(employee_id, last_name, first_name, middle_name, position, phone, hire_date):
    update_employee(employee_id, last_name, first_name, middle_name, position, phone, hire_date)


# Поставщики
def list_suppliers_full():
    return get_all_suppliers_full()

def get_supplier(supplier_id):
    return get_supplier_by_id(supplier_id)

def create_supplier(name, legal_address, actual_address, phone, email):
    add_supplier(name, legal_address, actual_address, phone, email)

def edit_supplier(supplier_id, name, legal_address, actual_address, phone, email):
    update_supplier(supplier_id, name, legal_address, actual_address, phone, email)


# Отчёты
def report_animals_condition():
    return get_animals_condition_report()

def report_medical_activity():
    return get_medical_activity_report()

def report_finance():
    return get_finance_report()

def report_attendance():
    return get_attendance_report()