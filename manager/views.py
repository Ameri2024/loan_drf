from django.shortcuts import get_object_or_404
from rest_framework import generics
from accounts.models import MyUser
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import SaveBalance, AdminPosts
from loans.models import Loans, Transactions, BankAccounts
from .serializers import SaveBalanceSerializer, AdminPostSerializer, AdminLoanSerializer, \
    AdminTransactionSerializer, BankAccountSerializer, LoanCreateSerializer


# === Save Balance Views ===
class SaveBalanceView(generics.ListCreateAPIView):
    queryset = SaveBalance.objects.all()
    serializer_class = SaveBalanceSerializer
    permission_classes = [IsAdminUser]


class UpdateBalanceView(generics.RetrieveUpdateAPIView):
    queryset = SaveBalance.objects.all()
    serializer_class = SaveBalanceSerializer
    permission_classes = [IsAdminUser]


class DeleteBalanceView(generics.DestroyAPIView):
    queryset = SaveBalance.objects.all()
    serializer_class = SaveBalanceSerializer
    permission_classes = [IsAdminUser]


# === Admin Posts Views ===
class AdminPostsView(generics.ListCreateAPIView):
    queryset = AdminPosts.objects.all()
    serializer_class = AdminPostSerializer
    permission_classes = [IsAdminUser]


class AdminPostDetailView(APIView):
    def get(self, request, *args, **kwargs):
        serializer = AdminPostSerializer(AdminPosts.objects.get(pk=kwargs['pk']))
        return Response(serializer.data)


class AdminPostUpdateView(generics.RetrieveUpdateAPIView):
    queryset = AdminPosts.objects.all()
    serializer_class = AdminPostSerializer
    permission_classes = [IsAdminUser]


class AdminDeletePostView(generics.DestroyAPIView):
    queryset = AdminPosts.objects.all()
    serializer_class = AdminPostSerializer
    permission_classes = [IsAdminUser]


# === Admin Loan Views ===
class LoanIndexView(generics.ListAPIView):
    queryset = Loans.objects.all()
    serializer_class = AdminLoanSerializer
    permission_classes = [IsAdminUser]


class LoanCreateView(generics.CreateAPIView):
    queryset = Loans.objects.all()
    serializer_class = LoanCreateSerializer
    permission_classes = [IsAdminUser]


class UpdateLoanView(generics.RetrieveUpdateAPIView):
    queryset = Loans.objects.all()
    serializer_class = AdminLoanSerializer
    permission_classes = [IsAdminUser]


class DeleteLoanView(generics.DestroyAPIView):
    queryset = Loans.objects.all()
    serializer_class = AdminLoanSerializer
    permission_classes = [IsAdminUser]


# === Admin Transaction Views ===
class AdminTransactionView(generics.ListAPIView):
    queryset = Transactions.objects.all()
    serializer_class = AdminTransactionSerializer
    permission_classes = [IsAdminUser]


class AdminTransactionUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Transactions.objects.all()
    serializer_class = AdminTransactionSerializer
    permission_classes = [IsAdminUser]


class AdminBankAccounts(generics.ListAPIView):
    serializer_class = BankAccountSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        national_code = self.kwargs['national_code']
        user = get_object_or_404(MyUser, national_code=national_code)
        return BankAccounts.objects.filter(user=user)
