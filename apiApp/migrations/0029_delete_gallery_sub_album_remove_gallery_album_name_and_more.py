# Generated by Django 4.0.3 on 2023-01-03 09:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apiApp', '0028_gallery_album_id_gallery_sub_album_id_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='gallery_sub_album',
        ),
        migrations.RemoveField(
            model_name='gallery',
            name='album_name',
        ),
        migrations.RemoveField(
            model_name='gallery',
            name='sub_album_id',
        ),
        migrations.RemoveField(
            model_name='gallery',
            name='sub_album_name',
        ),
    ]