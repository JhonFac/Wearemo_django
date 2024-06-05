from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APIRequestFactory, APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from .models import Customer, Loan, Payment, PaymentDetail
from .views import CustomerViewSet, LoanViewSet, PaymentDetailViewSet, PaymentViewSet


class TestCustomerViewSet(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.customer = Customer.objects.create(external_id='ABC123', score=1000)
        self.user = User.objects.create_user(username='admin', password='admin123')
        self.token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token))

    def test_retrieve_balance(self):
        url = reverse('customer-balance', kwargs={'external_id': self.customer.external_id})
        response = self.client.get(url)
        # Imprime la respuesta para depurar
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestLoanViewSet(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.customer = Customer.objects.create(external_id='ABC123', score=1000)
        self.user = User.objects.create_user(username='admin', password='admin123')
        self.token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token))

        self.factory = APIRequestFactory()
        self.loan = Loan.objects.create(external_id='L1', amount=1000, outstanding=1000, customer=self.customer)


    def test_get_loans_by_customer(self):
        url = reverse('loans-by-customer', kwargs={'external_id': self.customer.external_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_status_active(self):
        url = reverse('update status to active', kwargs={'external_id': self.loan.external_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_rejected_loan(self):
        url = reverse('Rejected loan', kwargs={'external_id': self.loan.external_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestPaymentViewSet(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.customer = Customer.objects.create(external_id='ABC123', score=1000)
        self.user = User.objects.create_user(username='admin', password='admin123')
        self.token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token))
        self.factory = APIRequestFactory()

    def test_get_payments_by_customer(self):
        url = reverse('payments-by-customer', kwargs={'external_id': self.customer.external_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestPaymentDetailViewSet(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.customer = Customer.objects.create(external_id='ABC123', score=1000)
        self.user = User.objects.create_user(username='admin', password='admin123')
        self.token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token))
        self.factory = APIRequestFactory()
        self.customer = Customer.objects.create(external_id='123', score=1000)
        self.loan = Loan.objects.create(external_id='456', amount=1000, outstanding=1000, customer=self.customer)
        self.payment = Payment.objects.create(external_id='789', total_amount=500, customer=self.customer)

    def test_create_payment_detail(self):
        url = reverse('paymentdetail-list')
        data = {'payment': self.payment.id, 'loan': self.loan.id, 'amount': 500}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
