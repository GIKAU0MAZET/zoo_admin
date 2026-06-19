from repositories.medical_records_repo import (
    get_treatment_requests_for_vet,
    get_medical_records_for_vet,
    add_medical_record,
    update_treatment_request_status,
    get_treatment_request_for_vet
)


def list_treatment_requests_for_vet(employee_id):
    return get_treatment_requests_for_vet(employee_id)


def list_medical_records_for_vet(employee_id):
    return get_medical_records_for_vet(employee_id)


def create_medical_record(request_id, animal_id, employee_id, name, date, condition):
    add_medical_record(request_id, animal_id, employee_id, name, date, condition)
    update_treatment_request_status(request_id, "Завершена")


def get_request_for_vet(request_id, employee_id):
    return get_treatment_request_for_vet(request_id, employee_id)