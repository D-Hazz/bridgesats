# Generated by Django 5.0.7 on 2024-09-17 09:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_remove_academie_description_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contact',
            old_name='email',
            new_name='email1',
        ),
    ]
