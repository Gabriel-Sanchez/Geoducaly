# Generated by Django 3.2.3 on 2023-07-18 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ciertoFalsoapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pregunta',
            name='imagen',
            field=models.ImageField(default=1, upload_to='preguntas/'),
            preserve_default=False,
        ),
    ]
