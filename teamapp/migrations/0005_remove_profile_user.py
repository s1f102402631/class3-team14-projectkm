# Generated by Django 5.1.4 on 2024-12-27 06:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teamapp', '0004_alter_customuser_table'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='user',
        ),
    ]
