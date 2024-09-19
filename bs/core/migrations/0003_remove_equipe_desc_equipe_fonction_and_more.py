# Generated by Django 5.0.7 on 2024-08-29 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_equipe'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='equipe',
            name='desc',
        ),
        migrations.AddField(
            model_name='equipe',
            name='fonction',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='equipe',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='equipe',
            name='github',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='equipe',
            name='whatsapp',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
