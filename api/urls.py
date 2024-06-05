from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from .views import CustomerViewSet, LoanViewSet, PaymentDetailViewSet, PaymentViewSet

router = DefaultRouter()
router.register(r'customers', CustomerViewSet)
router.register(r'loans', LoanViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'payment-details', PaymentDetailViewSet)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view (), name= 'token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name=' token_refresh'),
    path('', include(router.urls)),
    path('customers/<str:external_id>/balance/', CustomerViewSet.as_view({'get': 'retrieve_balance'}), name='customer-balance'),
    path('loans/by-customer/<str:external_id>/', LoanViewSet.as_view({'get': 'get_loans_by_customer'}), name='loans-by-customer'),
    path('payments/by-customer/<str:external_id>/', PaymentViewSet.as_view({'get': 'get_payments_by_customer'}), name='payments-by-customer'),
    path('loans/active/<str:external_id>/', LoanViewSet.as_view({'get': 'update_status_active'}), name='update status to active'),
    path('loans/rejected/<str:external_id>/', LoanViewSet.as_view({'get': 'rejected_loan'}), name='Rejected loan'),
]

