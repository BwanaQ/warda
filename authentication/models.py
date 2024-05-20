from django.contrib.auth.models import AbstractUser, PermissionsMixin, Group, Permission
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager
from locations.models import Address


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    ``created`` and ``modified`` fields.
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class User(AbstractUser, PermissionsMixin):
    IDENTIFICATION_TYPE_CHOICES = (
        (1, 'Passport'),
        (2, 'National ID'),
        (3, 'Birth Certificate')
    )
    role_type = models.ForeignKey(
        Role, on_delete=models.CASCADE, null=True, blank=True)
    identification_type = models.CharField(
        max_length=50, choices=IDENTIFICATION_TYPE_CHOICES, null=True, blank=True)
    id_no = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=50, null=True, blank=True)
    address = models.ForeignKey(
        Address, on_delete=models.CASCADE, null=True, blank=True)

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',  # Change the related name
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions_set',  # Change the related name
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Kin(TimeStampedModel):
    RELATION_CHOICES = (
        (1, 'Mother'),
        (2, 'Father'),
        (3, 'Sister'),
        (4, 'Brother'),
        (5, 'Wife'),
        (6, 'Husband')
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    relation = models.CharField(choices=RELATION_CHOICES, max_length=10)
    phone = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return f'{self.first_name}-{self.last_name}'


class Tenant(TimeStampedModel):
    """Represents a tenant"""
    INCOME_CHOICES = (
        (1, 'below 20,0000 ksh'),
        (2, '20,000-50,000 ksh'),
        (3, '50,000-100,000 ksh'),
        (4, 'above 100,000 ksh')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=50, null=True, blank=True)
    income = models.CharField(
        max_length=50, choices=INCOME_CHOICES, null=True, blank=True)
    kin = models.ForeignKey(Kin, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'{self.user.email}'


class Agent(TimeStampedModel):
    """Represents an agent"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email


class Landlord(TimeStampedModel):
    """Represents a landlord"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email


class ServicePRO(TimeStampedModel):
    """Represents a service provider"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email
