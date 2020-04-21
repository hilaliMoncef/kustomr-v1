from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.shortcuts import get_object_or_404



class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)



class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birthday = models.DateField(default=None, null=True, blank=True)
    is_vendor = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def get_customer(self, store=None):
        """
        A function used to get the customer associated.
        If a user is associated with several customers (same customer with different stores), we return the whole queryset.
        Else if there is only one user, we return this user
        """
        if store:
            customer = get_object_or_404(self.customers, store_linked__pk=store)
        else:
            if self.customers.count() > 1:
                customer = self.customers
            else:
                customer = self.customers.first()
        return customer