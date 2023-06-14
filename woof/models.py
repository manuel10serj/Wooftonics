from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Solicitante(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    nombre_completo = models.CharField(max_length = 200)
    direccion = models.CharField(max_length=200, null=True, blank=True)
    unidohace = models.DateTimeField(auto_now_add=True)

    def __str__ (self):
        return self.nombre_completo

class Categoria(models.Model):
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__ (self):
        return self.titulo

class Servicio(models.Model):
    titulo = models.CharField(max_length=30)
    slug = models.SlugField(unique=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to="servicios")
    precio_mercado = models.PositiveIntegerField()
    precio_venta = models.PositiveIntegerField()
    descripcion = models.TextField()
    garantia = models.CharField(max_length=300, null = True, blank = True)
    devolucion = models.CharField(max_length=300, null = True, blank = True)
    conteo_vistas = models.PositiveIntegerField(default = 0)

    def __str__(self):
        return self.titulo
    
class Contratar(models.Model):
    solicitante = models.ForeignKey(
        Solicitante, on_delete=models.SET_NULL, null=True, blank=True)
    total = models.PositiveIntegerField(default=0)
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str___(self):
        return "Solicitante: " + str(self.id)
    
class ContratarServicios(models.Model):
    contratar = models.ForeignKey(Contratar, on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    tasa = models.PositiveIntegerField()
    cantindad = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()

    def __str__(self):
        return "Solicitante: " + str(self.id) + "Contratar Servicios: " + str(self.id)
    
ORDER_STATUS = (
    ("Orden Recibida", "Orden Recibida"),
    ("Orden Procesada", "Orden Procesada"),
    ("Orden en Camino", "Orden en Camino"),
    ("Orden Completada", "Orden Compleda"),
    ("Orden Cancelada", "Orden Cancelada"),
)

class Orden(models.Model):
    contratar = models.OneToOneField(Contratar, on_delete=models.CASCADE)
    ordenado_por = models.CharField(max_length=200)
    direccion_de_envio = models.CharField(max_length=200)
    movil = models.CharField(max_length=10)
    email = models.EmailField(null=True, blank=True)
    subtotal = models.PositiveIntegerField()
    descuento = models.PositiveIntegerField()
    total = models.PositiveIntegerField()
    estado_de_orden = models.CharField(max_length=50, choices=ORDER_STATUS)
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Orden: " + str(self.id)
