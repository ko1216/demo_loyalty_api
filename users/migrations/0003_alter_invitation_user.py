# Generated by Django 5.0.4 on 2024-04-23 01:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_smscode_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users_invitation', to=settings.AUTH_USER_MODEL, verbose_name='user_owner'),
        ),
    ]
