# Generated by Django 3.2.3 on 2023-08-13 16:23

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('usersapp', '0001_initial'),
        ('cursosLeccionesapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Juegos_lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ruta_juego', models.TextField(blank=True)),
                ('nombre_juego', models.TextField(blank=True)),
                ('instrucciones', ckeditor.fields.RichTextField(blank=True)),
                ('score_max', models.DecimalField(decimal_places=2, max_digits=5)),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cursosLeccionesapp.lesson')),
            ],
        ),
        migrations.CreateModel(
            name='Score_juegos_lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('score', models.DecimalField(decimal_places=2, max_digits=5)),
                ('estudiante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usersapp.estudiante')),
                ('juego_lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gamesUnityapp.juegos_lesson')),
            ],
        ),
    ]
