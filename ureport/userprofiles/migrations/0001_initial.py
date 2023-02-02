# Generated by Django 4.0.8 on 2023-02-02 23:26

import dash.utils
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import functools


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='User')),
                ('contact_uuid', models.CharField(blank=True, db_index=True, default='', max_length=36, verbose_name='Contact UUID')),
                ('image', models.ImageField(help_text='The profile image file to use', upload_to=functools.partial(dash.utils.generate_file_path, *('userprofile',), **{}), verbose_name='Image')),
                ('password_reset_code', models.CharField(blank=True, default='', help_text='Confirmation code for the password reset', max_length=8, verbose_name='Confirmation code')),
                ('password_reset_expiry', models.DateTimeField(blank=True, help_text='Expiration date for the password reset', null=True, verbose_name='Expiration date')),
            ],
        ),
    ]
