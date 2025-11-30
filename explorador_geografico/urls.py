from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


from geografia import views as geografia_views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('geografia.urls')), 
]

handler403 = geografia_views.error_403
handler404 = geografia_views.error_404

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)