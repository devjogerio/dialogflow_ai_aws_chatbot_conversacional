from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TicketViewSet, BudgetViewSet, ChatAPIView

# Cria um roteador padrão do Django REST Framework
# O roteador gera automaticamente as URLs para os ViewSets registrados
router = DefaultRouter()

# Registra a rota 'tickets' apontando para o TicketViewSet
# Isso cria endpoints como /tickets/, /tickets/{id}/, etc.
router.register(r'tickets', TicketViewSet)

# Registra a rota 'budgets' apontando para o BudgetViewSet
router.register(r'budgets', BudgetViewSet)

# Define a lista de URLs do aplicativo 'tickets'
urlpatterns = [
    # Inclui todas as URLs geradas automaticamente pelo roteador
    path('', include(router.urls)),
    # Endpoint customizado para Chat
    path('chat/', ChatAPIView.as_view(), name='chat'),
]
