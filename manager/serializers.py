from rest_framework import serializers
from loans.models import Loans, Transactions, BankAccounts
from manager.models import SaveBalance, AdminPosts



class SaveBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaveBalance
        fields = '__all__'


class AdminPostSerializer(serializers.ModelSerializer):
    auther_full_name = serializers.CharField(source='auther.full_name', read_only=True)

    class Meta:
        model = AdminPosts
        fields = ['id', 'auther', 'auther_full_name', 'subject', 'post', 'created', 'is_active']


class AdminLoanSerializer(serializers.ModelSerializer):
    user_full_name = serializers.CharField(source='user.full_name', read_only=True)
    guaranteeing_full_name = serializers.CharField(source='guaranteeing.full_name', read_only=True)

    class Meta:
        model = Loans
        fields = '__all__'
        extra_kwargs = {
            'date_of_start': {
                'input_formats': ['%Y-%m-%d'], # فرمت تاریخ
                'format': 'YYYY-MM-DD'
            },
            'loan_amount': {
                'coerce_to_string': False # جلوگیری از تبدیل به رشته
            },
            'installment_amount': {
                'coerce_to_string': False
            }
        }


class AdminTransactionSerializer(serializers.ModelSerializer):
    user_full_name = serializers.CharField(source='user.full_name', read_only=True)

    class Meta:
        model = Transactions
        fields = '__all__'

class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccounts
        fields = '__all__'