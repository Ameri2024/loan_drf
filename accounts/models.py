from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager


# Customize User Models
class MyUser(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=255, unique=True)
    full_name = models.CharField(max_length=255)
    father_name = models.CharField(max_length=100)
    national_code = models.CharField(max_length=10, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=400)
    work_address = models.CharField(blank=True, max_length=400)
    phone_num = models.CharField(max_length=11, unique=True)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)

    objects = UserManager()
    USERNAME_FIELD = 'national_code'
    REQUIRED_FIELDS = ['email', 'phone_num', 'full_name']  # Use only for Super MyUser

    def __str__(self):
        return f'{self.full_name}'

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    def get_absolute_url(self):
        return reverse('update', kwargs={'national_code': self.national_code})
