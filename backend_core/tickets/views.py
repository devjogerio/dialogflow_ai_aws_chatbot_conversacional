from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Ticket, Budget
from .serializers import TicketSerializer, BudgetSerializer
from .rag_service import process_chat_message


class ChatAPIView(APIView):
    """
    Endpoint para interação via Chat (RAG com Bedrock + OpenSearch).
    Recebe: {"message": "texto da pergunta"}
    Retorna: {"response": "resposta gerada"}
    """

    def post(self, request):
        message = request.data.get('message')
        if not message:
            return Response({"error": "Mensagem é obrigatória"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            response_text = process_chat_message(message)
            return Response({"response": response_text})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ViewSet para o modelo Ticket
# Fornece automaticamente as operações CRUD (Create, Read, Update, Delete) via API


class TicketViewSet(viewsets.ModelViewSet):
    """
    Endpoint da API para gerenciamento de Chamados (Tickets).
    Permite listar, criar, recuperar, atualizar e deletar tickets.
    """
    # Define o conjunto de objetos (QuerySet) que será manipulado
    # Ordena os tickets pela data de criação (mais recentes primeiro)
    queryset = Ticket.objects.all().order_by('-created_at')

    # Define a classe Serializer usada para converter os dados
    serializer_class = TicketSerializer

# ViewSet para o modelo Budget
# Fornece automaticamente as operações CRUD para Orçamentos


class BudgetViewSet(viewsets.ModelViewSet):
    """
    Endpoint da API para gerenciamento de Orçamentos.
    Permite listar e criar orçamentos gerados pelo sistema.
    """
    # Define o conjunto de objetos (QuerySet) base
    queryset = Budget.objects.all().order_by('-created_at')

    # Define a classe Serializer usada
    serializer_class = BudgetSerializer
