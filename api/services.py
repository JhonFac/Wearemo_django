from .controller import (
    activate_loan_controller,
    create_customer,
    create_loan,
    get_customer_balance,
    get_loans_by_customer,
    get_payments_by_customer,
    process_payment,
    rejected_loan,
)
from .models import Customer


def create_payment(serializer):
    customer = serializer.validated_data['customer']
    total_debt = customer.total_debt()
    if total_debt <= 0:
        raise ValueError("Customer has no outstanding loans.")
    if serializer.validated_data['total_amount'] > total_debt:
        raise ValueError("Payment amount exceeds total debt.")

    payment = serializer.save()
    process_payment(payment)
    return payment
