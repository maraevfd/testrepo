# Generated by Django 2.2.7 on 2019-12-11 16:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portalapp', '0010_auto_20191211_1629'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Wage',
            new_name='Salary',
        ),
    ]