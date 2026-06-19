from datetime import datetime
from repositories.treatment_requests_repo import (
    get_all_treatment_requests,
    get_treatment_request_by_id,
    add_treatment_request,
    update_treatment_request
)


def list_treatment_requests():
    return get_all_treatment_requests()


def create_treatment_request(
        employee_id,
        animal_id,
        veterinarian_id,
        title,
        status,
        zoo_id
):
    today = datetime.now()
    add_treatment_request(
        today,
        employee_id,
        animal_id,
        veterinarian_id,
        title,
        status,
        zoo_id
    )
    
def get_treatment_request(request_id):
    return get_treatment_request_by_id(request_id)


def edit_treatment_request(
        request_id,
        animal_id,
        veterinarian_id,
        title,
        status
):
    update_treatment_request(
        request_id,
        animal_id,
        veterinarian_id,
        title,
        status
    )