# Generated by Django 4.0.3 on 2023-01-14 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiApp', '0035_rename_h2_small_banner_p'),
    ]

    operations = [
        migrations.CreateModel(
            name='suscribeModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.TextField(blank=True)),
                ('last_name', models.TextField(blank=True)),
                ('phone_no', models.TextField(blank=True)),
                ('email', models.TextField(blank=True)),
            ],
        ),
    ]
