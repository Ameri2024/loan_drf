from django.contrib.auth.models import BaseUserManager

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, national_code, email, phone_num, full_name, father_name, date_of_birth, address, work_address,
                    password=None, profile_image=None):
        if not national_code:
            raise ValueError("MyUser must have an National Code Number")
        if not email:
            raise ValueError("Users must have an email address")
        if not phone_num:
            raise ValueError("Users must have a Phone Number")

        user = self.model(
            national_code=national_code,
            email=self.normalize_email(email),
            phone_num=phone_num,
            full_name=full_name,
            father_name=father_name,
            date_of_birth=date_of_birth,
            address=address,
            work_address=work_address,
            profile_image=profile_image
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, national_code, email, phone_num, full_name, password=None, father_name=None,
                         date_of_birth=None, address=None, work_address=None, profile_image=None):
        user = self.create_user(
            national_code=national_code,
            email=email,
            phone_num=phone_num,
            full_name=full_name,
            father_name=father_name or "",
            date_of_birth=date_of_birth,
            address=address or "",
            work_address=work_address or "",
            password=password,
            profile_image=profile_image
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user


