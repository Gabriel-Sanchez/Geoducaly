# Generated by Django 3.2.3 on 2023-10-16 21:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cursosLeccionesapp', '0002_lesson_mostrar'),
        ('ciertoFalsoapp', '0004_auto_20231010_2103'),
    ]

    operations = [
        migrations.AddField(
            model_name='test_true_false',
            name='grupofk',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cursosLeccionesapp.grupo'),
        ),
    ]
