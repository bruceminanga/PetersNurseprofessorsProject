# Generated by Django 5.0.6 on 2024-06-24 11:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0003_writer'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='writer',
            name='is_writer',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='writer',
            name='expertise',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='writer',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='writer_profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('proposal', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending', max_length=20)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.order')),
                ('writer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.writer')),
            ],
        ),
    ]
