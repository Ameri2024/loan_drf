from rest_framework import serializers
from .models import Loans, Transactions, BankAccounts


class LoanSerializer(serializers.ModelSerializer):
    calculate_payment_num = serializers.SerializerMethodField()
    payment_amount = serializers.SerializerMethodField()
    rest_debt_amount = serializers.SerializerMethodField()

    class Meta:
        model = Loans
        fields = '__all__'

    def get_calculate_payment_num(self, obj):
        return obj.calculate_payment_num()

    def get_payment_amount(self, obj):
        return obj.payment_amount()

    def get_rest_debt_amount(self, obj):
        return obj.rest_debt_amount()


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
