from django.urls import path, re_path
from . import views

app_name = 'manager'

urlpatterns = [
    path('loan/index', views.LoanIndexView.as_view(), name='loan_index'),
    path('loan/create', views.LoansCreationView.as_view(), name='loan_create'),
    path('loan/update/<int:pk>/', views.UpdateLoanView.as_view(), name='update_loan'),
    path('loan/delete/<int:pk>/', views.DeleteLoanView.as_view(), name='delete_loan'),
    path('transaction', views.AdminTransactionView.as_view(), name='all_transaction'),
    path('transactions/update/<int:pk>', views.AdminTransactionUpdateView.as_view(), name='admin_transaction_update'),
    path('save/balance', views.SaveBalanceView.as_view(), name='save_balance'),
    path('save/balance/update/<int:pk>', views.UpdateBalanceView.as_view(), name='update_balance'),
    path('save/balance/delete/<int:pk>', views.DeleteBalanceView.as_view(), name='delete_balance'),
    path('posts/', views.AdminPostsView.as_view(), name='all_posts'),
    path('post/update/<int:pk>', views.AdminPostUpdateView.as_view(), name='post_update'),
    path('post/delete/<int:pk>', views.AdminDeletePostView.as_view(), name='post_delete'),
    re_path('bank/accounts/(?P<national_code>[0-9]{10})', views.AdminBankAccounts.as_view(), name='admin_bank_accounts'),

]
