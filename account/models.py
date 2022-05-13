from operator import mod
from pyexpat import model
from turtle import update
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


# Create your models here.

NATIONS = (
    ('INDIA','INDIA'),
    ('PAKISTAN','PAKISTAN'),
    ('BANGLADESH','BANGLADESH'),
    ('NEPAL','NEPAL')
)

## Creating user manager custom
class MyUserManager(BaseUserManager):
    def create_user(self, email, date_of_birth, name, nationality, password=None,password2=None):
        """
        Creates and saves a User with the given email, date of
        birth password ,contact_number, nationality,.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
            name=name,
            nationality=nationality
            
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email,date_of_birth, name, nationality, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth, password name,contact_number, nationality,
        """
        user = self.create_user(
            email,
            date_of_birth=date_of_birth,
            name=name,
            nationality=nationality,
            password=password
            
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
    
    


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    date_of_birth = models.DateField()
    name = models.CharField(max_length=100)
    nationality=  models.CharField(choices=NATIONS,max_length=15)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['date_of_birth','name','nationality']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin