from django.contrib.auth.models import (
    BaseUserManager
)


class UserManager(BaseUserManager):

    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('User must have a phone number')
        user = self.model(
            phone_number=phone_number,
            password=self.make_random_password(),
            role='user',
            **extra_fields,
        )
        user.save(using=self._db)

        return user

    def create_superuser(self, phone_number, password=None):
        user = self.create_user(
            phone_number=phone_number,
            password=password,
        )
        user.role = 'admin'
        user.save(using=self._db)

        return user
