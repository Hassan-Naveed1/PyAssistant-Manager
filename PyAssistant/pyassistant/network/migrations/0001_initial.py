# Generated by Django 4.2.19 on 2025-03-17 03:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pyassistant', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NetworkData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upload_speed', models.FloatField()),
                ('download_speed', models.FloatField()),
                ('total_usage', models.FloatField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pyassistant.host')),
            ],
        ),
    ]
