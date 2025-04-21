from rest_framework import serializers
from .models import Loans, Transactions, BankAccounts


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loans
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = ['id', 'lend', 'receipt', 'loan', 'verify']
        read_only_fields = ['user', 'verify']


class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccounts
        fields = '__all__'
        read_only_fields = ['user']
