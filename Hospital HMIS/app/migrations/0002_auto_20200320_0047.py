# Generated by Django 2.2.11 on 2020-03-19 22:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='opdevent',
            old_name='data_of_attendance',
            new_name='date_of_attendance',
        ),
    ]