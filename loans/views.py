from django.shortcuts import render
from rest_framework import status, generics, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Loans, Transactions, BankAccounts
from .serializers import LoanSerializer, TransactionSerializer, BankAccountSerializer


class UserLoanView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        loans = Loans.objects.filter(user=request.user)
        serializer = LoanSerializer(loans, many=True)
        return Response(serializer.data)


class LoansDetailView(RetrieveAPIView):
    queryset = Loans.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # فقط وام‌های متعلق به کاربر وارد شده
        return Loans.objects.filter(user=self.request.user)


class TransactionsCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # ست کردن کاربر لاگین شده
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransactionUpdateView(UpdateAPIView):
    queryset = Transactions.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        # اجازه ویرایش فقط برای صاحب تراکنش
        if self.request.user != serializer.instance.user:
            raise PermissionDenied("شما اجازه ویرایش این تراکنش را ندارید.")
        serializer.save()


class TransactionDeleteView(DestroyAPIView):
    queryset = Transactions.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        if self.request.user != instance.user:
            raise PermissionDenied("شما اجازه حذف این تراکنش را ندارید.")
        instance.delete()


class BankAccountsView(generics.ListCreateAPIView):
    serializer_class = BankAccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return BankAccounts.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BankAccountUpdateView(generics.UpdateAPIView):
    serializer_class = BankAccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return BankAccounts.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class BankAccountDeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return BankAccounts.objects.filter(user=self.request.user)
