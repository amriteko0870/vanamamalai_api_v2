# Generated by Django 4.0.3 on 2022-12-24 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiApp', '0014_rootpagestatus'),
    ]

    operations = [
        migrations.AddField(
            model_name='landing_page',
            name='background_color',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]