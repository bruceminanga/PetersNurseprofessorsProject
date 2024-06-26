# Generated by Django 3.2.9 on 2024-06-17 09:09

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=50, null=True, unique=True)),
                ('valid_from', models.DateTimeField()),
                ('valid_to', models.DateTimeField()),
                ('discount', models.IntegerField(help_text='Percentage vaule (0 to 100)', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('active', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('academic_level', models.CharField(default='1', max_length=20)),
                ('type_of_service', models.CharField(default='1', max_length=30)),
                ('type_of_paper', models.CharField(default='Unknown', max_length=255)),
                ('subject_area', models.CharField(default='1', max_length=20)),
                ('title', models.CharField(default='Untitled', max_length=255)),
                ('paper_instructions', models.TextField(default='')),
                ('additional_material', models.FileField(blank=True, null=True, upload_to='files/%Y/%m/%d/')),
                ('paper_format', models.CharField(default='Unknown', max_length=20)),
                ('number_of_pages', models.CharField(default='1', max_length=20)),
                ('number_of_pages_increment', models.IntegerField(default=1)),
                ('currency', models.CharField(default='USD', max_length=20)),
                ('sources', models.IntegerField(default=0)),
                ('powerpoint_slides', models.IntegerField(default=0)),
                ('deadline', models.CharField(default='None', max_length=20)),
                ('writer_category', models.CharField(default='Standard', max_length=20)),
                ('preferred_writers_id', models.IntegerField(blank=True, null=True)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('writer', models.CharField(default='Untitled', max_length=255)),
                ('words', models.IntegerField(default=0)),
                ('amount_due', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('name', models.CharField(max_length=191)),
                ('email', models.EmailField(max_length=254)),
                ('postal_code', models.IntegerField(default=0)),
                ('address', models.CharField(default='Unknown', max_length=191)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('paid', models.BooleanField(default=False)),
                ('bidding', models.BooleanField(default=False)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed'), ('in_progress', 'In Progress'), ('cancelled', 'Cancelled'), ('approved', 'Approved'), ('revision', 'Revision'), ('editing', 'Editing')], default='pending', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=191)),
                ('price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('slug', models.SlugField()),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Referral',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('referrer', models.CharField(max_length=191)),
                ('referred', models.CharField(max_length=191)),
                ('amount_earned', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(default='empty', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('description', models.CharField(max_length=255)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('balance_after', models.DecimalField(decimal_places=2, max_digits=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender', models.CharField(max_length=191)),
                ('subject', models.CharField(default='No Subject', max_length=255)),
                ('body', models.TextField(default='No Content')),
                ('date_sent', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_read', models.BooleanField(default=False)),
                ('receiver', models.CharField(max_length=191)),
                ('content', models.TextField(default='No Content')),
                ('sent_at', models.DateTimeField(auto_now_add=True)),
                ('read', models.BooleanField(default=False)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LineItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('quantity', models.IntegerField()),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.product')),
            ],
        ),
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=5)),
                ('expiry_date', models.DateField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
