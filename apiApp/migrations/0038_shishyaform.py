# Generated by Django 4.0.3 on 2023-02-24 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiApp', '0037_suscribemodel_city_suscribemodel_country_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='shishyaForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.TextField()),
            ],
        ),
    ]