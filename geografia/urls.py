from django.urls import path
from . import views

urlpatterns = [

    path('', views.lista_paises, name='lista_paises'),
    path('pais/<int:pais_id>/', views.detalle_pais, name='detalle_pais'),
    path('lugar/marcar/<int:lugar_id>/', views.marcar_conocido, name='marcar_conocido'),
    path('lugar/nuevo/', views.crear_lugar, name='crear_lugar'),
    path('lugar/<int:pk>/editar/', views.editar_lugar, name='editar_lugar'),
    path('lugar/<int:pk>/eliminar/', views.eliminar_lugar, name='eliminar_lugar'),
    
    # Rutas de Autenticación
    path('registro/', views.registro_usuario, name='registro'),
    path('login/', views.login_usuario, name='login'),
    path('logout/', views.logout_usuario, name='logout'),
]