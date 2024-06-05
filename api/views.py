from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Customer, Loan, Payment, PaymentDetail
from .serializers import (
    CustomerSerializer,
    LoanSerializer,
    PaymentDetailSerializer,
    PaymentSerializer,
)
from .services import (
    activate_loan_controller,
    create_customer,
    create_loan,
    create_payment,
    get_customer_balance,
    get_loans_by_customer,
    get_payments_by_customer,
    rejected_loan,
)


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        create_customer(serializer)

    @swagger_auto_schema(responses={200: 'Balance Retrieved'})
    def retrieve_balance(self, request, external_id=None):
        customer = get_object_or_404(Customer, external_id=external_id)
        data = get_customer_balance(customer)
        return Response(data, status=status.HTTP_200_OK)


class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            create_loan(serializer)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @swagger_auto_schema(responses={200: 'Get loans by customer'})
    def get_loans_by_customer(self, request, external_id=None):
        loans, error, status_code = get_loans_by_customer(external_id)
        if error:
            return Response(error, status=status_code)
        serializer = LoanSerializer(loans, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(responses={200: 'Activate Loan'})
    def update_status_active(self, request, external_id=None):
        response = activate_loan_controller(external_id)
        return Response(response['data'], status=response['status'])

    @swagger_auto_schema(responses={200: 'Activate Loan'})
    def rejected_loan(self, request, external_id=None):
        response = rejected_loan(external_id)
        return Response(response['data'], status=response['status'])


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            create_payment(serializer)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


    @swagger_auto_schema(responses={200: 'Get payments by customer'})
    def get_payments_by_customer(self, request, external_id=None):
        payments, error, status_code = get_payments_by_customer(external_id)
        if error:
            return Response(error, status=status_code)
        return Response(payments)


class PaymentDetailViewSet(viewsets.ModelViewSet):
    queryset = PaymentDetail.objects.all()
    serializer_class = PaymentDetailSerializer
    permission_classes = [IsAuthenticated]
