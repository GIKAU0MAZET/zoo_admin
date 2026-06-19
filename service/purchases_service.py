from repositories.purchases_repo import (
    get_all_purchases,
    add_purchase
)

from repositories.purchase_items_repo import (
    copy_request_items_to_purchase
)


def list_purchases():
    return get_all_purchases()


def create_purchase(request_id):

    purchase_id = add_purchase(request_id)

    copy_request_items_to_purchase(
        request_id,
        purchase_id
    )