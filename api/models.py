from django.db import models
from django.db.models import Sum

CUSTOMER_STATUS_CHOICES = [
    (1, 'Active'),
    (2, 'Inactive'),
]

LOAN_STATUS_CHOICES = [
    (1, 'pending'),
    (2, 'active'),
    (3, 'rejected'),
    (4, 'paid'),
]

PAYMENT_STATUS_CHOICES = [
    (1, 'completed'),
    (2, 'rejected'),
]

class Customer(models.Model):
    external_id = models.CharField(max_length=60, unique=True)
    score = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.SmallIntegerField(choices=CUSTOMER_STATUS_CHOICES, default=1)
    preapproved_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.external_id

    def total_debt(self):
        loans = self.loans.filter(status__in=[1, 2])
        return loans.aggregate(total_outstanding=Sum('outstanding'))['total_outstanding'] or 0

    def available_amount(self):
        return self.score - self.total_debt()

class Loan(models.Model):
    external_id = models.CharField(max_length=60, unique=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    contract_version = models.CharField(max_length=30, blank=True, null=True)
    status = models.SmallIntegerField(choices=LOAN_STATUS_CHOICES, default=1)
    taken_at = models.DateTimeField(null=True, blank=True)
    outstanding = models.DecimalField(max_digits=12, decimal_places=2)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='loans')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.external_id


class Payment(models.Model):
    external_id = models.CharField(max_length=60, unique=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.SmallIntegerField(choices=PAYMENT_STATUS_CHOICES, default=1)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='payments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    paid_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.external_id


class PaymentDetail(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='details')
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='payment_details')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.payment.external_id} - {self.loan.external_id}'
