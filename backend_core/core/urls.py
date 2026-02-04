from django.contrib import admin
from django.urls import path, include

# Definição das URLs principais do projeto
urlpatterns = [
    # URL para o painel administrativo do Django
    path('admin/', admin.site.urls),
    
    # Inclui as URLs da API do aplicativo 'tickets'
    # Prefixo 'api/' para organizar os endpoints da API
    path('api/', include('tickets.urls')),
]
