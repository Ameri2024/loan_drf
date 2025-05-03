from django.shortcuts import render
from rest_framework import status, generics, permissions
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.generics import RetrieveAPIView, UpdateAPIView, DestroyAPIView, get_object_or_404
from rest_framework.pagination import PageNumberPagination
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
        if self.request.user.is_admin:
            return Loans.objects.all()
        return Loans.objects.filter(user=self.request.user)


class TransactionListCreateView(generics.ListCreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):

        return Transactions.objects.filter(user=self.request.user) \
            .select_related('loan')

    def perform_create(self, serializer):
        """Auto-set user and validate loan ownership"""
        loan = get_object_or_404(
            Loans,
            id=self.request.data.get('loan'),
            user=self.request.user
        )
        serializer.save(user=self.request.user)

    # Your existing implementation is correct, but we can add pagination
    pagination_class = PageNumberPagination
    page_size = 20


class TransactionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'patch', 'delete']  # Disable PUT

    def get_queryset(self):

        return Transactions.objects.filter(user=self.request.user) \
            .select_related('loan')

    def perform_update(self, serializer):
        """Add custom update validation if needed"""
        instance = self.get_object()
        # Example: Prevent updating verified transactions
        if instance.verify:
            raise ValidationError("Verified transactions cannot be modified")
        serializer.save()

    def perform_destroy(self, instance):
        """Add custom delete validation if needed"""
        # Example: Prevent deleting verified transactions
        if instance.verify:
            raise ValidationError("Verified transactions cannot be deleted")
        instance.delete()


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


class BankAccountDetailView(generics.RetrieveAPIView):
    queryset = BankAccounts.objects.all()
    serializer_class = BankAccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return BankAccounts.objects.filter(user=self.request.user)
