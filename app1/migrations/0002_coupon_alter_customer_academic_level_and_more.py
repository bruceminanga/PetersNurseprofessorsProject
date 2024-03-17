# Generated by Django 5.0.2 on 2024-03-16 09:52

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, unique=True)),
                ('valid_from', models.DateTimeField()),
                ('valid_to', models.DateTimeField()),
                ('discount', models.IntegerField(help_text='Percentage vaule (0 to 100)', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('active', models.BooleanField()),
            ],
        ),
        migrations.AlterField(
            model_name='customer',
            name='academic_level',
            field=models.CharField(default=1, max_length=20),
        ),
        migrations.AlterField(
            model_name='customer',
            name='currency',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='customer',
            name='deadline',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='customer',
            name='number_of_pages',
            field=models.CharField(default=1, max_length=20),
        ),
        migrations.AlterField(
            model_name='customer',
            name='paper_instructions',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='customer',
            name='powerpoint_slides',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='customer',
            name='sources',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='customer',
            name='subject_area',
            field=models.CharField(default=1, max_length=20),
        ),
        migrations.AlterField(
            model_name='customer',
            name='type_of_paper',
            field=models.CharField(default=1, max_length=20),
        ),
        migrations.AlterField(
            model_name='customer',
            name='type_of_service',
            field=models.CharField(default=1, max_length=30),
        ),
        migrations.AlterField(
            model_name='customer',
            name='writer_category',
            field=models.CharField(max_length=20),
        ),
    ]
