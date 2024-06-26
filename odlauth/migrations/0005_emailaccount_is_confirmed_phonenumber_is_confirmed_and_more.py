# Generated by Django 5.0.4 on 2024-04-25 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('odlauth', '0004_user_date_joined_user_is_staff_user_is_superuser_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailaccount',
            name='is_confirmed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='phonenumber',
            name='is_confirmed',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
