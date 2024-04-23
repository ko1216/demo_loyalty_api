from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from users.managers import UserManager

NULLABLE = {'blank': True, 'null': True}


class UserRoles(models.TextChoices):
    user = 'user'
    admin = 'admin'


class User(AbstractBaseUser, PermissionsMixin):
    username = None

    phone_number = PhoneNumberField(verbose_name='phone_number', unique=True)
    role = models.CharField(max_length=9, choices=UserRoles.choices,
                            default=UserRoles.user, verbose_name='role')
    invite_code = models.CharField(max_length=6, verbose_name='invite_code', **NULLABLE)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    @property
    def is_superuser(self):
        return self.role == UserRoles.admin

    @property
    def is_staff(self):
        return self.role == UserRoles.admin

    @property
    def is_user(self):
        return self.role == UserRoles.user

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class Invitation(models.Model):
    code = models.CharField(max_length=6, unique=True)
    is_activated = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='user_owner', related_name='users_invitation', **NULLABLE)
    activated_by = models.ManyToManyField(User, verbose_name='activated_by_users', related_name='activated_invitations')


class SMSCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    code = models.CharField(max_length=4, verbose_name='verify_code')
    created_at = models.DateTimeField(auto_now_add=True)
