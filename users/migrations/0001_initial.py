# Generated by Django 3.0.5 on 2020-04-22 09:01

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128)),
                ('email', models.EmailField(max_length=254)),
                ('age', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('reference', models.CharField(blank=True, default=uuid.uuid4, max_length=100, primary_key=True, serialize=False, unique=True)),
                ('account', models.CharField(max_length=128)),
                ('date', models.DateField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=16)),
                ('type', models.CharField(choices=[('inflow', 'inflow'), ('outflow', 'outflow')], max_length=10)),
                ('category', models.CharField(max_length=128)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='users.User')),
            ],
        ),
    ]