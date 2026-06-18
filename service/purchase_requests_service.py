from repositories.purchase_requests_repo import (
    get_all_purchase_requests,
    get_purchase_request_by_id,
    add_purchase_request,
    update_purchase_request
)


def list_purchase_requests():
    return get_all_purchase_requests()

def get_purchase_request(request_id):
    return get_purchase_request_by_id(request_id)


def create_purchase_request(
        date,
        employee_id,
        executor_id,
        status
):
    add_purchase_request(
        date,
        employee_id,
        executor_id,
        status
    )
    
def edit_purchase_request(
        request_id,
        date,
        executor_id,
        status
):
    update_purchase_request(
        request_id,
        date,
        executor_id,
        status
    )