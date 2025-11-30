from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Lugar 


class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']



# Se utiliza para que el usuario 'staff' o administrador pueda crear y editar Lugares.
class LugarForm(forms.ModelForm):
    class Meta:
        model = Lugar 
        fields = ['pais', 'nombre', 'ciudad', 'categoria', 'descripcion', 'imagen']