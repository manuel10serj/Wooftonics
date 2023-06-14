from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.views.generic import View, TemplateView, CreateView, FormView
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import VerificarForm, RegistrarForm, IniciarSesionForm
from typing import Any, Dict
from .models import *

# Create your views here.

class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['myname'] = "Manuel Alcalá"
        context['lista_servicios'] = Servicio.objects.all().order_by("-id")
        return context

class TodoServicios(TemplateView):
    template_name = "todoservicios.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['todoservicios'] = Categoria.objects.all()
        return context
    
class DetalleServicio(TemplateView):
    template_name = "detalleServicio.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url_slug = self.kwargs['slug']
        servicio = Servicio.objects.get(slug = url_slug)
        servicio.conteo_vistas += 1
        servicio.save()
        context['servicio'] = servicio
        return context
    

class AgregarServicioSolicitado(TemplateView):
    template_name = "solicitudes.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obten el id del servicio url solicitado
        servicio_id = self.kwargs["ser_id"]
        # Obten servicio
        servicio_obj = Servicio.objects.get(id=servicio_id)

        # Verifica si el servicio existe
        contratar_id = self.request.session.get("contratar_id", None)
        if contratar_id:
            contratar_obj = Contratar.objects.get(id=contratar_id)
            this_servicio_contratado = contratar_obj.contratarServicio_set.filter(
                servicio=servicio_obj)
            
            # Servicio ya existentes contratados
            if this_servicio_contratado.exists():
                contratarServicio = this_servicio_contratado.last()
                contratarServicio.cantindad += 1
                contratarServicio.subtotal += servicio_obj.precio_venta
                contratarServicio.save()
                servicio_obj.total += servicio_obj.precio_venta
                contratarServicio.save() 
            # Nuevo Servicio agregado a contratados
            else:
                contratarServicio = ContratarServicios.objects.create(
                    contratar = contratar_obj, servicio = servicio_obj, tasa = servicio_obj.precio_venta, cantindad = 1, subtotal = servicio_obj.precio_venta)
                contratar_obj.total += servicio_obj.precio_venta
                contratar_obj.save()

        else:
            contratar_obj = Contratar.objects.create(total=0)
            self.request.session["contratar_id"] = contratar_obj.id
            contratarServicio = ContratarServicios.objects.create(
                contratar = contratar_obj, servicio = servicio_obj, tasa = servicio_obj.precio_venta, cantindad = 1, subtotal = servicio_obj.precio_venta)
            contratar_obj.total += servicio_obj.precio_venta
            contratar_obj.save()
        return context            

class AdministrarServicios(View):
    def get(self, request, *args, **kwargs):
        cp_id = self.kwargs["cp_id"]
        action = request.GET.get("action")
        cp_obj = ContratarServicios.objects.get(id=cp_id)
        contratar_obj = cp_obj.contratar

        if action == "inc":
            cp_obj.cantindad += 1
            cp_obj.subtotal += cp_obj.tasa
            cp_obj.save()
            contratar_obj.total += cp_obj.tasa
            contratar_obj.save()
        elif action == "dcr":
            cp_obj.cantindad -= 1
            cp_obj.subtotal -= cp_obj.tasa
            cp_obj.save()
            contratar_obj.total -= cp_obj.tasa
            contratar_obj.save()
            if cp_obj.cantindad == 0:
                cp_obj.delete()
        elif action == "eli":
            contratar_obj.total -= cp_obj.tasa
            contratar_obj.save()
            cp_obj.delete()
        else:
            pass
        return redirect("woof:mis-servicios")


class EliminarServicios(View):
    def get(self, request, *args, **kwargs):
        contratar_id = request.session.get("contratar_id", None)
        if contratar_id:
            contratar = Contratar.objects.get(id=contratar_id)
            contratar.contratarServicio_set.all().delete()
            contratar.total = 0
            contratar.save()
        return redirect("woof:mis-servicios") 


class MisServicios(TemplateView):
    template_name = "miservicios.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contratar_id = self.request.session.get("contratar_id", None)
        if contratar_id:
            contratar = Contratar.objects.get(id=contratar_id)
        else: 
            contratar = None
        context['contratar'] = contratar
        return context


class Verificar(CreateView):
    template_name = "verificar.html"
    form_class = VerificarForm
    success_url = reverse_lazy("woof:home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contratar_id = self.request.session.get("contratar_id", None)
        if contratar_id:
            contratar_obj = Contratar.objects.get(id=contratar_id)
        else: 
            contratar_obj = None
        context["contratar"] = contratar_obj
        return context
    
    def form_valid(self, form):
        contratar_id = self.request.session.get("contratar_id")
        if contratar_id:
            contratar_obj = Contratar.objects.get(id=contratar_id)
            form.instance.contratar = contratar_obj
            form.instance.subtotal = contratar_obj.total
            form.instance.descuento = 0
            form.instance.total = contratar_obj.total
            form.instance.estado_de_orden = "Orden Recibida"
            del self.request.session["contratar_id"]
        else:
             return redirect("woof:home")
        return super().form_valid(form)

class Registrar(CreateView):
    template_name = "registrar.html"
    form_class = RegistrarForm
    success_url = reverse_lazy("woof:home")

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("email")
        user = User.objects.create_user(username, email, password)
        form.instance.user = user
        login(self.request, user)
        return super().form_valid(form)
    
class IniciarSesion(FormView):
    template_name = "iniciarSesion.html"
    form_class = IniciarSesionForm
    success_url = reverse_lazy("woof:home")
    
    def form_valid(self, form):
        uname = form.cleaned_data.get("username")
        pword = form.cleaned_data.get("password")
        usr = authenticate(username=uname, password=pword)
        if usr is not None and usr.solicitante:
            login(self.request, usr)
        else: 
            return render(self.request, self.template_name, {"form": self.form_class, "error": "Usuario Invalido"})
        
        return super().form_valid(form)

    
class CerrarSesion(View):
    def get(self, request):
        logout(request)
        return redirect("woof:home")

class AboutView(TemplateView):
    template_name = "about.html"

class ContactanosView(TemplateView):
    template_name = "contacto.html"