# Generated by Django 5.0.4 on 2024-04-18 19:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('odlauth', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='EmailAccounts',
            new_name='EmailAccount',
        ),
        migrations.RenameModel(
            old_name='PhoneNumbers',
            new_name='PhoneNumber',
        ),
    ]
