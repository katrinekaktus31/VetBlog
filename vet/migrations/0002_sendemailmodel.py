# Generated by Django 3.2.7 on 2021-10-24 14:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vet', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SendEmailModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_name', models.CharField(blank=True, max_length=150, verbose_name="Ім'я")),
                ('client_email', models.EmailField(max_length=70, unique=True, verbose_name='E-mail')),
                ('content', models.TextField(blank=True, verbose_name='Текст повідомлення')),
                ('vet_member', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Ветеринарний лікар')),
            ],
        ),
    ]
