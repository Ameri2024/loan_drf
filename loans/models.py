from django.db import models
from accounts.models import MyUser
from django_jalali.db import models as jalali_models


class Loans(models.Model):
    TYPE_CHOICES = [
        ('normal', 'معمولی'),
        ('urgent', 'اضطراری'),
        ('saving', 'پس انداز'),
    ]
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    loan_amount = models.IntegerField()  # مبلغ وام
    date_of_start = models.DateField()
    installment_amount = models.IntegerField()  # مبلغ قسط
    installment_num = models.SmallIntegerField()  # تعداد قسط
    payment_num = models.SmallIntegerField()  # تعداد قسط پرداختی
    guaranteeing = models.ForeignKey(MyUser, on_delete=models.DO_NOTHING, related_name='guaranteeing')
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='normal')
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Loans'

    def __str__(self):
        return f"{self.user} - {self.get_type_display()} - {self.loan_amount}"

    def calculate_payment_num(self):
        # Access the related transactions for this loan
        transactions = self.transactions.filter(verify=True)
        # Count the number of verified transactions
        payment_num = transactions.count()
        return payment_num

    def payment_amount(self):
        transactions = self.transactions.filter(verify=True)
        # Extract the 'lend' values from the queryset and then sum them
        payment_amount = sum(transaction.lend for transaction in transactions)
        return payment_amount

    def rest_debt_amount(self):
        rest_debt_amount = self.loan_amount - self.payment_amount()
        return rest_debt_amount

    def save2(self, *args, **kwargs):
        # Calculate payment_num
        self.payment_num = self.calculate_payment_num()
        # Call the original save method
        super(Loans, self).save(*args, **kwargs)


class Transactions(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    lend = models.IntegerField()
    receipt = models.ImageField(upload_to='receipts/')
    created = jalali_models.jDateTimeField(auto_now_add=True)
    verify = models.BooleanField(default=False)
    loan = models.ForeignKey(Loans, on_delete=models.CASCADE, related_name='transactions', default=None)

    def __str__(self):
        return f'{self.user} -- {self.lend}'

    class Meta:
        ordering = ['-created']


# Create your models here.
class BankAccounts(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    bank_name = models.CharField(max_length=100)
    account_num = models.CharField(max_length=20, blank=True)
    shaba_num = models.CharField(max_length=26, blank=True)
    cart_num = models.CharField(max_length=16)

    class Meta:
        verbose_name_plural = "Bank Accounts"

    def __str__(self):
        return f'{self.user} --- {self.bank_name} --- {self.account_num}'

