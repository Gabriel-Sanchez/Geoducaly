# Generated by Django 3.2.3 on 2024-02-12 22:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('defapp', '0003_alter_datos_thumbnail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='datos',
            name='course',
        ),
    ]
