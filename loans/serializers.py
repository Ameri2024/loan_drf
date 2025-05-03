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
    # Add read_only=True here
    created = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ", read_only=True)

    # Keep other fields the same...
    user_full_name = serializers.CharField(source='user.full_name', read_only=True)
    loan_type = serializers.CharField(source='loan.type', read_only=True)
    loan_amount = serializers.IntegerField(source='loan.loan_amount', read_only=True)
    loan = serializers.PrimaryKeyRelatedField(
        queryset=Loans.objects.all(),
        required=True
    )

    class Meta:
        model = Transactions
        fields = [
            'id', 'user', 'user_full_name', 'lend', 'receipt', 'loan',
            'loan_type', 'loan_amount', 'verify', 'created'
        ]
        read_only_fields = ['user', 'verify', 'created', 'user_full_name', 'loan_type', 'loan_amount']
        extra_kwargs = {
            'lend': {'min_value': 1000}
        }

    def validate_loan(self, value):
        if value.user != self.context['request'].user:
            raise serializers.ValidationError("Invalid loan selection")
        return value


class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccounts
        fields = '__all__'
        read_only_fields = ['user']
