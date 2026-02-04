from django.db import models

# Modelo que representa um Ticket de Suporte no sistema
# Armazena informações sobre solicitações de clientes, status e descrição do problema
class Ticket(models.Model):
    # Opções de status disponíveis para o ticket (Enumeração)
    STATUS_CHOICES = [
        ('OPEN', 'Aberto'),           # Ticket recém-criado
        ('IN_PROGRESS', 'Em Andamento'), # Ticket sendo atendido
        ('RESOLVED', 'Resolvido'),    # Problema solucionado
        ('CLOSED', 'Fechado')         # Ticket finalizado
    ]

    # Nome do cliente que abriu o chamado (Obrigatório)
    customer_name = models.CharField(max_length=255, verbose_name="Nome do Cliente")
    
    # ID ou identificador único do cliente no sistema externo (Opcional)
    customer_id = models.CharField(max_length=100, verbose_name="ID do Cliente", blank=True, null=True)
    
    # Descrição detalhada do problema relatado pelo cliente (Texto longo)
    problem_description = models.TextField(verbose_name="Descrição do Problema")
    
    # Status atual do ticket, com valor padrão 'OPEN'
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OPEN', verbose_name="Status")
    
    # Data e hora da criação do ticket (Automático)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de Abertura")
    
    # Data e hora da última atualização do ticket (Automático)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última Atualização")

    def __str__(self):
        # Representação em string do objeto (exibido no Admin do Django)
        return f"Ticket #{self.id} - {self.customer_name}"

    class Meta:
        # Nome amigável para exibição no painel administrativo
        verbose_name = "Chamado"
        verbose_name_plural = "Chamados"


# Modelo que representa um Orçamento gerado pelo sistema
# Armazena detalhes sobre serviços cotados e valores
class Budget(models.Model):
    # Nome do cliente para quem o orçamento foi gerado
    customer_name = models.CharField(max_length=255, verbose_name="Nome do Cliente")
    
    # Tipo de serviço solicitado (ex: Consultoria, Manutenção)
    service_type = models.CharField(max_length=200, verbose_name="Tipo de Serviço")
    
    # Valor total calculado para o orçamento (Decimal para precisão monetária)
    total_value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor Total (R$)")
    
    # Caminho ou URL para o arquivo PDF gerado (Opcional)
    pdf_url = models.URLField(verbose_name="URL do PDF", blank=True, null=True)
    
    # Data de criação do orçamento
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de Geração")

    def __str__(self):
        return f"Orçamento #{self.id} - {self.service_type}"

    class Meta:
        verbose_name = "Orçamento"
        verbose_name_plural = "Orçamentos"
