# Generated by Django 4.0.3 on 2022-12-31 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiApp', '0020_vanamamalai_other_temple_tab_show_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='vanamamalai_mutt_branches_tab',
            name='show_status',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]