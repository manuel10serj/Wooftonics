# Generated by Django 3.2.19 on 2023-06-11 23:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=200)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Contratar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.PositiveIntegerField(default=0)),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Solicitante',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_completo', models.CharField(max_length=200)),
                ('direccion', models.CharField(blank=True, max_length=200, null=True)),
                ('unidohace', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Servicio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=30)),
                ('slug', models.SlugField(unique=True)),
                ('imagen', models.ImageField(upload_to='servicios')),
                ('precio_mercado', models.PositiveIntegerField()),
                ('precio_venta', models.PositiveIntegerField()),
                ('descripcion', models.TextField()),
                ('garantia', models.CharField(blank=True, max_length=300, null=True)),
                ('devolucion', models.CharField(blank=True, max_length=300, null=True)),
                ('conteo_vistas', models.PositiveIntegerField(default=0)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='woof.categoria')),
            ],
        ),
        migrations.CreateModel(
            name='Orden',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordenado_por', models.CharField(max_length=200)),
                ('direccion_de_envio', models.CharField(max_length=200)),
                ('movil', models.CharField(max_length=10)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('subtotal', models.PositiveIntegerField()),
                ('descuento', models.PositiveIntegerField()),
                ('total', models.PositiveIntegerField()),
                ('estado_de_orden', models.CharField(choices=[('Orden Recibida', 'Orden Recibida'), ('Orden Procesada', 'Orden Procesada'), ('Orden en Camino', 'Orden en Camino'), ('Orden Completada', 'Orden Compleda'), ('Orden Cancelada', 'Orden Cancelada')], max_length=50)),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
                ('contratar', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='woof.contratar')),
            ],
        ),
        migrations.CreateModel(
            name='ContratarServicios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tasa', models.PositiveIntegerField()),
                ('cantindad', models.PositiveIntegerField()),
                ('subtotal', models.PositiveIntegerField()),
                ('contratar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='woof.contratar')),
                ('servicio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='woof.servicio')),
            ],
        ),
        migrations.AddField(
            model_name='contratar',
            name='solicitante',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='woof.solicitante'),
        ),
    ]
