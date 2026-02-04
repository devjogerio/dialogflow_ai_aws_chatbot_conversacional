from rest_framework import serializers
from .models import Ticket, Budget

# Serializer para o modelo Ticket
# Converte instâncias do modelo Ticket para JSON e valida dados de entrada
class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        # Define o modelo associado a este serializer
        model = Ticket
        # Inclui todos os campos do modelo na serialização
        fields = '__all__'

# Serializer para o modelo Budget
# Converte instâncias do modelo Budget para JSON e valida dados de entrada
class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        # Define o modelo associado a este serializer
        model = Budget
        # Inclui todos os campos do modelo na serialização
        fields = '__all__'
