# Generated by Django 4.0.8 on 2023-02-20 09:43

import dash.utils
from django.db import migrations, models
import functools


class Migration(migrations.Migration):

    dependencies = [
        ('userprofiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userprofile',
            options={'verbose_name': 'User profile', 'verbose_name_plural': 'Use profiles'},
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(help_text='The profile image file to use', upload_to=functools.partial(dash.utils.generate_file_path, *('userprofiles',), **{}), verbose_name='Image'),
        ),
    ]
