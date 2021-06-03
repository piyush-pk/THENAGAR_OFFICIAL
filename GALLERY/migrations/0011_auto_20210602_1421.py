# Generated by Django 3.2.3 on 2021-06-02 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GALLERY', '0010_remove_album_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photo',
            name='tags',
        ),
        migrations.AddField(
            model_name='photo',
            name='caption',
            field=models.CharField(default='', max_length=250),
            preserve_default=False,
        ),
    ]
