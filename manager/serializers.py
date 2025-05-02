from rest_framework import serializers
from loans.models import Loans, Transactions, BankAccounts
from manager.models import SaveBalance, AdminPosts
from rest_framework.validators import UniqueTogetherValidator


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
    calculate_payment_num = serializers.SerializerMethodField()
    payment_amount = serializers.SerializerMethodField()
    rest_debt_amount = serializers.SerializerMethodField()

    class Meta:
        model = Loans
        fields = '__all__'
        extra_kwargs = {
            'loan_amount': {'min_value': 0},
            'installment_amount': {'min_value': 0},
            'installment_num': {'min_value': 1},
            'payment_num': {'min_value': 0}
        }

    def get_payment_num(selfself, obj):
        return obj.calculate_payment_num()

    def get_payment_amount(self, obj):
        return obj.payment_amount()

    def get_rest_debt_amount(self, obj):
        return obj.rest_debt_amount()


class LoanCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loans
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Loans.objects.all(),
                fields=['user', 'date_of_start'],
                message="این کاربر قبلاً وام با این تاریخ شروع داشته است"
            )
        ]

    def validate(self, data):
        if data['installment_amount'] * data['installment_num'] != data['loan_amount']:
            raise serializers.ValidationError(
                "مبلغ قسط ضربدر تعداد اقساط باید برابر مبلغ وام باشد"
            )
        return data


class AdminTransactionSerializer(serializers.ModelSerializer):
    user_full_name = serializers.CharField(source='user.full_name', read_only=True)

    class Meta:
        model = Transactions
        fields = '__all__'


class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccounts
        fields = '__all__'
