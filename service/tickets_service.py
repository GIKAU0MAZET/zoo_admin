from datetime import datetime
from repositories.tickets_repo import get_all_tickets, add_ticket

TICKET_PRICES = {
    "Взрослый": 500,
    "Детский": 300,
}


def list_tickets():
    return get_all_tickets()


def create_ticket(ticket_type, quantity, employee_id, zoo_id):
    today = datetime.now()
    price = TICKET_PRICES.get(ticket_type, 0)
    add_ticket(today, ticket_type, price, quantity, employee_id, zoo_id)