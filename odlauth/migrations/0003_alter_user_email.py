# Generated by Django 5.0.4 on 2024-04-25 17:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('odlauth', '0002_rename_emailaccounts_emailaccount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='odlauth.emailaccount'),
        ),
    ]
