# Generated by Django 4.0.3 on 2022-12-05 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiApp', '0007_jeeyars_tab'),
    ]

    operations = [
        migrations.AddField(
            model_name='jeeyars',
            name='banner_heading',
            field=models.TextField(default='Jeeyar Parampara'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='jeeyars',
            name='banner_image',
            field=models.TextField(default='media/img/vanamamalai_temple/banner.png'),
            preserve_default=False,
        ),
    ]
