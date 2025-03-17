# Generated by Django 4.2.19 on 2025-03-17 02:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hostname', models.CharField(max_length=255, unique=True)),
                ('ip_address', models.GenericIPAddressField(unique=True)),
                ('username', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=255)),
            ],
        ),
    ]
