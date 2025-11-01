from django.contrib import admin
from django.urls import path, include # Importamos 'include' 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')), # Redirige la raíz a las URLs de la app 'blog'
]