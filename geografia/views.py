from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.views.decorators.http import require_POST 
from .models import Pais, Lugar, Conocimiento 
from .forms import RegistroForm, LugarForm


# --- Utilidad para verificar si el usuario es admin del proyecto ---
def es_admin_proyecto(user):
    return user.is_staff 


# --- Vistas de Autenticación (Req. 5) ---

def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registro exitoso. Inicia sesión para continuar.')
            return redirect('login')
    else:
        form = RegistroForm()
    return render(request, 'register.html', {'form': form})


def login_usuario(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f'Bienvenido {user.username}')
            return redirect('lista_paises') 
        else:
            messages.error(request, 'Credenciales inválidas')
    return render(request, 'login.html')


@login_required
def logout_usuario(request):
    logout(request)
    messages.info(request, 'Sesión cerrada correctamente.')
    return render(request, 'logout.html')


# --- Vistas principales (Req. 3 y 4) ---

# Vista para listar todos los países (Req. 3 - Contenido Dinámico)
def lista_paises(request):
    paises = Pais.objects.all()
    return render(request, 'geografia/lista_paises.html', {'paises': paises})


@login_required 
# Vista para el detalle del País y el cálculo del porcentaje (Req. 3, 4)
def detalle_pais(request, pais_id):
    # Asegura que el País exista
    pais = get_object_or_404(Pais, pk=pais_id)
    
    # 1. Obtener todos los lugares del país (Total)
    lugares_del_pais = Lugar.objects.filter(pais=pais)
    total_lugares = lugares_del_pais.count()
    
    # 2. Obtener los lugares conocidos por el usuario actual (Req. 4)
    lugares_conocidos = Conocimiento.objects.filter(
        usuario=request.user, 
        lugar__in=lugares_del_pais
    )
    lugares_conocidos_count = lugares_conocidos.count()
    
    # 3. Cálculo del porcentaje (Req. 4 - Lógica de Negocio)
    porcentaje = 0
    if total_lugares > 0:
        porcentaje = round((lugares_conocidos_count / total_lugares) * 100, 2)
        
    context = {
        'pais': pais,
        'lugares': lugares_del_pais,
        'lugares_conocidos_ids': [c.lugar.id for c in lugares_conocidos], 
        'porcentaje': porcentaje,
        'total_lugares': total_lugares,
    }

    return render(request, 'geografia/detalle_pais.html', context)


@login_required
@require_POST
# Vista para procesar la acción "Marcar como conocido" (Req. 4 - Procesamiento)
def marcar_conocido(request, lugar_id):
    lugar = get_object_or_404(Lugar, pk=lugar_id)
    
    # Crea el registro de conocimiento (el unique_together previene duplicados)
    Conocimiento.objects.get_or_create(usuario=request.user, lugar=lugar)
    
    messages.success(request, f"¡{lugar.nombre} ha sido marcado como conocido!")
    # Redirige de vuelta a la página del país para ver el porcentaje actualizado
    return redirect('detalle_pais', pais_id=lugar.pais.pk)


# --- CRUD restringido al admin del proyecto (Req. 5, 6) ---

@login_required
def crear_lugar(request):
    # Control de acceso: solo staff puede crear (Req. 5)
    if not request.user.is_staff: 
        raise PermissionDenied
    if request.method == 'POST':
        form = LugarForm(request.POST, request.FILES) 
        if form.is_valid():
            form.save()
            messages.success(request, 'Lugar creado correctamente.')
            return redirect('lista_paises') 
    else:
        form = LugarForm()
    return render(request, 'geografia/crear_lugar.html', {'form': form})


@login_required
def editar_lugar(request, pk):
    # Control de acceso: solo staff puede editar (Req. 5)
    if not request.user.is_staff: 
        raise PermissionDenied
    lugar = get_object_or_404(Lugar, pk=pk) 
    form = LugarForm(request.POST or None, request.FILES or None, instance=lugar)
    if form.is_valid():
        form.save()
        messages.success(request, 'Lugar actualizado.')
        # Redirige al detalle del país
        return redirect('detalle_pais', pais_id=lugar.pais.pk) 
    return render(request, 'geografia/editar_lugar.html', {'form': form, 'lugar': lugar})


@login_required
def eliminar_lugar(request, pk):
    # Control de acceso: solo staff puede eliminar (Req. 5)
    if not request.user.is_staff: 
        raise PermissionDenied
    lugar = get_object_or_404(Lugar, pk=pk) 
    if request.method == 'POST':
        lugar.delete()
        messages.warning(request, 'Lugar eliminado correctamente.')
        return redirect('lista_paises')
    return render(request, 'geografia/eliminar_lugar.html', {'lugar': lugar})


# --- Errores personalizados (Req. 5) ---

def error_403(request, exception=None):
    return render(request, 'geografia/403.html', status=403)

def error_404(request, exception=None):
    return render(request, 'geografia/404.html', status=404)