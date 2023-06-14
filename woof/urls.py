from django.urls import path
from .views import *

app_name = "woof"
urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("about/", AboutView.as_view(), name="about"),
    path("contactanos/", ContactanosView.as_view(), name="contacto"),
    path("todos-servicios/", TodoServicios.as_view(), name="todoservicios"),
    path("servicio/<slug:slug>/", DetalleServicio.as_view(), name="detalle"),
    path("serviciosSolicitado-<int:ser_id>/", AgregarServicioSolicitado.as_view(), name="solicitudes"),
    path("mis.servicios/", MisServicios.as_view(), name="mis-servicios"),
    path("administrar-servicios/<int:cp_id>/", AdministrarServicios.as_view(), name="adminServ"),
    path("eliminar-servicios/", EliminarServicios.as_view(), name="elimServ"),
    path("verificar/", Verificar.as_view(), name="verificar"),
    path("registrar/", Registrar.as_view(), name="registrar"), 
    path("cerrarSecion/", CerrarSesion.as_view(), name="cerrarSesion"),
    path("iniciarSesion/", IniciarSesion.as_view(), name="iniciarSesion"),

]