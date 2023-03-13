# Generated by Django 4.0.8 on 2023-03-09 13:18

import dash.utils
from django.db import migrations, models
import functools


class Migration(migrations.Migration):

    dependencies = [
        ('userbadges', '0003_remove_userbadge_accepted_on_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='badgetype',
            name='image',
            field=models.ImageField(blank=True, help_text='The badge image file', null=True, upload_to=functools.partial(dash.utils.generate_file_path, *('userbadges',), **{}), verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='badgetype',
            name='is_visible',
            field=models.BooleanField(db_index=True, default=True, verbose_name='Display badges of this type'),
        ),
    ]