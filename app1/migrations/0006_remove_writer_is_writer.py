# Generated by Django 5.0.6 on 2024-06-24 15:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0005_writer_application_status_writerapplication'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='writer',
            name='is_writer',
        ),
    ]