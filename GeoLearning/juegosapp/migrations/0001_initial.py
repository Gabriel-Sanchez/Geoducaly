# Generated by Django 3.2.3 on 2023-08-05 20:53

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
            name='CardPar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='card_images')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('size', models.IntegerField()),
                ('image', models.ImageField(upload_to='country_images')),
            ],
        ),
        migrations.CreateModel(
            name='ElegirRespuesta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('correcta', models.BooleanField(default=False, verbose_name='¿es esta la pregunta correcta?')),
                ('texto', models.TextField(verbose_name='texto de la respuesta')),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('summary', models.TextField()),
                ('difficulty_level', models.CharField(max_length=20)),
                ('leccion', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cursosLeccionesapp.lesson')),
            ],
        ),
        migrations.CreateModel(
            name='ListQuiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.TextField(verbose_name='titulo del quiz')),
                ('alt', models.TextField(blank=True)),
                ('picture', models.ImageField(blank=True, null=True, upload_to='triviaImage')),
                ('leccion', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cursosLeccionesapp.lesson')),
            ],
        ),
        migrations.CreateModel(
            name='Pregunta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.TextField(verbose_name='texto de la pregunta')),
                ('listquices', models.IntegerField(null=True)),
                ('max_puntaje', models.DecimalField(decimal_places=2, default=1, max_digits=6, verbose_name='maximo puntaje')),
                ('alt', models.TextField(blank=True)),
                ('picture', models.ImageField(blank=True, null=True, upload_to='TriviaPreguntaimage')),
                ('listquiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listquiz', to='juegosapp.listquiz')),
            ],
        ),
        migrations.CreateModel(
            name='UserNumQuiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Num_veces_jugadas', models.IntegerField(default=0, null=True)),
                ('listquiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='juegosapp.listquiz')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usersapp.estudiante')),
            ],
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='juegosapp.game')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usersapp.estudiante')),
            ],
        ),
        migrations.CreateModel(
            name='QuizUsuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('puntaje_total', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Puntaje total')),
                ('Num_jugada', models.IntegerField(null=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usersapp.estudiante')),
            ],
        ),
        migrations.CreateModel(
            name='PreguntasRespondidas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('correcta', models.BooleanField(default=False, verbose_name='¿es esta la respuesta correcta?')),
                ('puntaje_obtenido', models.DecimalField(decimal_places=2, default=0, max_digits=6, verbose_name='Puntaje Obtenido')),
                ('pregunta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='juegosapp.pregunta')),
                ('quizUser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='intentos', to='juegosapp.quizusuario')),
                ('respuesta', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='juegosapp.elegirrespuesta')),
            ],
        ),
        migrations.CreateModel(
            name='ijuegos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('iframe', models.TextField(blank=True)),
                ('type', models.IntegerField(blank=True)),
                ('url', models.CharField(max_length=320)),
                ('alt', models.TextField(blank=True)),
                ('picture', models.ImageField(blank=True, null=True, upload_to='juegosimage')),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cursosLeccionesapp.course')),
            ],
        ),
        migrations.AddField(
            model_name='elegirrespuesta',
            name='pregunta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='opciones', to='juegosapp.pregunta'),
        ),
    ]