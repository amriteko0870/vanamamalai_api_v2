# Generated by Django 4.0.3 on 2022-12-21 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiApp', '0013_rename_jeeyar_id_vanamamalai_education_tab_education_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='rootPageStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('status', models.TextField()),
            ],
        ),
    ]
