# Generated by Django 4.0.3 on 2023-01-12 07:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apiApp', '0034_card_section_h1_card_section_p_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='small_banner',
            old_name='h2',
            new_name='p',
        ),
    ]
