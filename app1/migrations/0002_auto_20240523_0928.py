# Generated by Django 3.2.9 on 2024-05-23 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='writer',
            field=models.CharField(default='Untitled', max_length=255),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed'), ('In Progress', 'In Progress')], max_length=50),
        ),
    ]