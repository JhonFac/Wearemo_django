from django.utils import timezone
from rest_framework import status

from .models import Customer, Loan, Payment, PaymentDetail
from .serializers import LoanSerializer


def create_customer(serializer):
    return serializer.save(status=1)

def get_customer_balance(customer):
    return {
        "external_id": customer.external_id,
        "score": customer.score,
        "available_amount": customer.available_amount(),
        "total_debt": customer.total_debt()
    }

def create_loan(serializer):

    # Obtener el estado del préstamo
    status = serializer.validated_data.get('status')
    # Verificar si el préstamo está en estado "pending"
    if status == 1:  # "pending"
        raise ValueError("The status is pending, you must update the status to active.")
    else:
        # Si no está en estado "pending", solo guarda el préstamo
        customer = serializer.validated_data['customer']
        if customer.total_debt() + serializer.validated_data['amount'] > customer.score:
            raise ValueError("Loan amount exceeds available credit limit.")
        return serializer.save()

def process_payment(payment):
    customer = payment.customer
    amount_paid = payment.total_amount
    for loan in customer.loans.filter(status=2).order_by('created_at'):
        if loan.outstanding <= amount_paid:
            payment_detail = PaymentDetail(payment=payment, loan=loan, amount=loan.outstanding)
            payment_detail.save()
            amount_paid -= loan.outstanding
            loan.outstanding = 0
            loan.status = 4
        else:
            payment_detail = PaymentDetail(payment=payment, loan=loan, amount=amount_paid)
            payment_detail.save()
            loan.outstanding -= amount_paid
            amount_paid = 0
        loan.save()
        if amount_paid <= 0:
            break
    payment.status = 1
    payment.save()

def get_loans_by_customer(external_id):
    try:
        customer = Customer.objects.get(external_id=external_id)
    except Customer.DoesNotExist:
        return None, {"error": "Customer not found."}, 404

    loans = Loan.objects.filter(customer=customer)
    return loans, None, 200


def get_payments_by_customer(external_id):
    try:
        customer = Customer.objects.get(external_id=external_id)
    except Customer.DoesNotExist:
        return None, {"error": "Customer not found."}, 404

    payments = Payment.objects.filter(customer=customer)
    payment_details = PaymentDetail.objects.filter(payment__in=payments)

    result = []
    for payment_detail in payment_details:
        result.append({
            "external_id": payment_detail.payment.external_id,
            "customer_external_id": external_id,
            "loan_external_id": payment_detail.loan.external_id,
            "payment_date": payment_detail.payment.paid_at.strftime("%Y-%m-%d"),
            "status": payment_detail.payment.status,
            "total_amount": payment_detail.payment.total_amount,
            "payment_amount": payment_detail.amount,
        })

    return result, None, 200

def activate_loan_controller(external_id):
    try:
        loan = Loan.objects.get(external_id=external_id)
    except Loan.DoesNotExist:
        return {"data": {"error": "Loan does not exist"}, "status": status.HTTP_404_NOT_FOUND}
    loan.status = 2
    loan.taken_at = timezone.now()
    loan.save()
    serializer = LoanSerializer(loan)
    return {"data": serializer.data, "status": status.HTTP_200_OK}


def rejected_loan(external_id):
    try:
        loan = Loan.objects.get(external_id=external_id)
    except Loan.DoesNotExist:
        return {"data": {"error": "Loan does not exist"}, "status": status.HTTP_404_NOT_FOUND}
    if loan.status != 1:
        data = {"message": "Loan cannot be rejected because the status has already changed."}
        return {"data": data, "status": status.HTTP_400_BAD_REQUEST}

    loan.status = 3
    loan.save()
    serializer = LoanSerializer(loan)
    return {"data": serializer.data, "status": status.HTTP_200_OK}

