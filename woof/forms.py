from django import forms
from .models import Orden, Solicitante
from django.contrib.auth.models import User

class VerificarForm(forms.ModelForm):
     class Meta:
        model = Orden
        fields = ["ordenado_por", "direccion_de_envio", "movil", "email"]

class RegistrarForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.CharField(widget=forms.EmailInput())
     
    class Meta:
        model = Solicitante
        fields = ["username", "password", "email", "nombre_completo", "direccion"]

    def clean_username(self):
        uname = self.cleaned_data.get("username")
        if User.objects.filter(username=uname).exists():
            raise forms.ValidationError(
                "¡Este nombre de Usuario ya Existe!")
        return uname

class IniciarSesionForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())