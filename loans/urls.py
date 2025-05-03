from django.urls import path
from . import views

app_name = 'loans'

urlpatterns = [
    path('', views.UserLoanView.as_view(), name='user_loans'),
    path('loan/detail/<int:pk>', views.LoansDetailView.as_view(), name='load_details'),
    path('transactions/', views.TransactionListCreateView.as_view(), name='transactions-list-create'),
    path('transactions/<int:pk>', views.TransactionDetailView.as_view(), name='transaction-detail'),
    path('transactions/update/<int:pk>', views.TransactionUpdateView.as_view(), name='transaction_update'),
    path('transactions/delete/<int:pk>', views.TransactionDeleteView.as_view(), name='transaction_delete'),
    path('bank/accounts/', views.BankAccountsView.as_view(), name='bank-accounts'),
    path('bank/accounts/detial/<int:pk>', views.BankAccountDetailView.as_view(), name='bank_account_details'),
    path('bank/accounts/update/<int:pk>', views.BankAccountUpdateView.as_view(), name='bank_account_update'),
    path('bank/accounts/delete/<int:pk>', views.BankAccountDeleteView.as_view(), name='bank_account_delete'),
]
