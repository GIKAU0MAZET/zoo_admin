from repositories.medical_records_repo import get_all_medical_records, add_medical_record


def list_medical_records():
    return get_all_medical_records()


def create_medical_record(request_id, animal_id, employee_id, name, date, condition):
    add_medical_record(request_id, animal_id, employee_id, name, date, condition)