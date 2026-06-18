from repositories.purchase_request_items_repo import (
    get_request_items,
    add_request_item
)


def list_request_items(request_id):
    return get_request_items(request_id)


def create_request_item(
        request_id,
        supplier_id,
        food_id,
        quantity
):
    add_request_item(
        request_id,
        supplier_id,
        food_id,
        quantity
    )