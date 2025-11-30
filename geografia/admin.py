from django.contrib import admin
from .models import Pais, Lugar, Conocimiento 


# 1. Administración del modelo País
@admin.register(Pais)
class PaisAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)
      
# Esta clase permite gestionar los lugares y vincularlos a un País.
@admin.register(Lugar)
class LugarAdmin(admin.ModelAdmin):
    # Añadimos 'pais' a la visualización
    list_display = ('nombre', 'pais', 'ciudad', 'categoria', 'fecha_creacion') 
    # Añadimos 'pais__nombre' para buscar por nombre del país
    search_fields = ('nombre', 'ciudad', 'categoria', 'pais__nombre')
    # Permite filtrar los lugares por País y Categoría
    list_filter = ('pais', 'categoria')


# Esta clase permite auditar qué usuario conoce qué lugar.
@admin.register(Conocimiento)
class ConocimientoAdmin(admin.ModelAdmin):
    # Muestra el usuario y el lugar que conoce
    list_display = ('usuario', 'lugar', 'fecha_conocido')
    search_fields = ('usuario__username', 'lugar__nombre')
    list_filter = ('usuario', 'fecha_conocido')