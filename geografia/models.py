from django.db import models
from django.contrib.auth.models import User 

# 1. Modelo País
# Este modelo lista todos los países disponibles para explorar.
class Pais(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Países"

# 2. Modelo Lugar (Experiencia o Punto de Interés)
class Lugar(models.Model):
    # Relación de uno a muchos: Un país puede tener muchos lugares
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE, related_name='lugares') 
    
    nombre = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=50) 
    categoria = models.CharField(max_length=50) # Ej: "Histórico", "Natural", "Cultural"
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='lugares/', blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} ({self.pais.nombre})"

    class Meta:
        verbose_name_plural = "Lugares"


# 3. Modelo Conocimiento (La Lógica de Negocio Requerida)
# Es una relación de muchos a muchos con información adicional (quién, qué y cuándo).
class Conocimiento(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conocimientos')
    lugar = models.ForeignKey(Lugar, on_delete=models.CASCADE)
    fecha_conocido = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Esto es crucial: asegura que un usuario solo pueda "conocer" un lugar una vez.
        unique_together = ('usuario', 'lugar') 
        verbose_name_plural = "Conocimientos"

    def __str__(self):
        return f"{self.usuario.username} conoce {self.lugar.nombre}"