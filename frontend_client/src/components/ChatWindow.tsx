"use client";
import React, { useState, useEffect, useRef } from 'react';

// Interface que define a estrutura de dados de uma mensagem no chat
interface Message {
  id: string; // Identificador único da mensagem
  text: string; // Conteúdo textual da mensagem
  sender: 'user' | 'bot'; // Identifica o remetente (usuário ou sistema)
  timestamp: Date; // Carimbo de data/hora do envio
}

/**
 * Componente ChatWindow
 *
 * Este componente renderiza a interface principal do chatbot.
 * Ele gerencia o estado da conversa, a entrada do usuário e a exibição das respostas.
 * Implementa padrões de UX como "Optimistic UI" (exibe mensagem do usuário imediatamente)
 * e feedback de carregamento (loading state).
 */
const ChatWindow: React.FC = () => {
  // --- Estados do Componente ---

  // Lista de mensagens trocadas na sessão atual
  const [messages, setMessages] = useState<Message[]>([]);

  // Valor atual do campo de entrada de texto
  const [inputText, setInputText] = useState('');

  // Estado que indica se o bot está processando uma resposta
  const [isLoading, setIsLoading] = useState(false);

  // Referência para o elemento final da lista, usada para rolagem automática
  const messagesEndRef = useRef<HTMLDivElement>(null);
  // Referência para o input, para focar após o envio
  const inputRef = useRef<HTMLInputElement>(null);

  // --- Efeitos Colaterais (Side Effects) ---

  // Rola a visualização para a última mensagem sempre que a lista 'messages' for atualizada
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Foca no input ao carregar o componente
  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  // --- Handlers de Eventos ---

  // Função acionada ao enviar uma nova mensagem
  const handleSendMessage = async (e?: React.FormEvent) => {
    // Previne o comportamento padrão de recarregamento do formulário
    if (e) e.preventDefault();

    // Validação básica: não envia se estiver vazio ou apenas espaços
    if (!inputText.trim()) return;

    // Constrói o objeto da mensagem do usuário
    const userMessage: Message = {
      id: Date.now().toString(),
      text: inputText,
      sender: 'user',
      timestamp: new Date(),
    };

    // Atualiza a UI otimisticamente (adiciona a mensagem antes da resposta do servidor)
    setMessages((prev: Message[]) => [...prev, userMessage]);

    // Limpa o campo de input e define estado de carregamento
    setInputText('');
    setIsLoading(true);

    // Mantém o foco no input para digitação contínua
    inputRef.current?.focus();

    try {
      // Chamada real para a API do Backend
      // Utiliza a variável de ambiente NEXT_PUBLIC_API_URL para definir o endpoint
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

      const res = await fetch(`${apiUrl}/api/chat/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: userMessage.text }),
      });

      if (!res.ok) {
        throw new Error(`Erro na API: ${res.status}`);
      }

      const data = await res.json();
      const responseText =
        data.response || 'Desculpe, não consegui processar sua solicitação.';

      // Constrói o objeto da mensagem de resposta do Bot
      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: responseText,
        sender: 'bot',
        timestamp: new Date(),
      };

      // Adiciona a resposta do bot à lista de mensagens
      setMessages((prev: Message[]) => [...prev, botMessage]);
    } catch (error) {
      console.error('Erro ao enviar mensagem:', error);
      // Adiciona mensagem de erro visual para o usuário
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: 'Desculpe, ocorreu um erro ao conectar com o servidor. Tente novamente mais tarde.',
        sender: 'bot',
        timestamp: new Date(),
      };
      setMessages((prev: Message[]) => [...prev, errorMessage]);
    } finally {
      // Finaliza o estado de carregamento independente do sucesso ou falha
      setIsLoading(false);
    }
  };

  // --- Renderização (JSX) ---
  return (
    <div className="flex flex-col h-[600px] max-w-md mx-auto bg-white rounded-xl shadow-2xl overflow-hidden border border-gray-200 font-sans">
      {/* Cabeçalho do Chat */}
      <div className="bg-indigo-600 p-4 text-white flex items-center justify-between shadow-md">
        <div>
          <h2 className="font-bold text-lg">Nexus AI Suporte</h2>
          <p className="text-xs text-indigo-200">
            Assistente Virtual Inteligente
          </p>
        </div>
        <span className="text-xs bg-green-400 px-2 py-1 rounded-full text-indigo-900 font-bold uppercase tracking-wider">
          Online
        </span>
      </div>

      {/* Área de Visualização de Mensagens (Scrollable) */}
      <div
        className="flex-1 overflow-y-auto p-4 bg-gray-50 space-y-4"
        role="log"
        aria-live="polite"
        aria-atomic="false"
        aria-label="Histórico do Chat"
      >
        {/* Mensagem de boas-vindas condicional (apenas se não houver mensagens) */}
        {messages.length === 0 && (
          <div className="text-center text-gray-500 mt-10 text-sm p-6 bg-gray-100 rounded-lg mx-4">
            <p className="font-semibold mb-2">👋 Olá! Sou o Nexus AI.</p>
            <p>
              Estou conectado à base de conhecimento da empresa. Pergunte sobre
              manuais, abra chamados ou peça orçamentos.
            </p>
          </div>
        )}

        {/* Renderização da lista de mensagens */}
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[80%] p-3 rounded-lg text-sm shadow-sm leading-relaxed ${
                msg.sender === 'user'
                  ? 'bg-indigo-600 text-white rounded-br-none' // Estilo para mensagem do usuário
                  : 'bg-white border border-gray-200 text-gray-800 rounded-bl-none' // Estilo para mensagem do bot
              }`}
            >
              {msg.text}
              <div
                className={`text-[10px] mt-1 text-right ${msg.sender === 'user' ? 'text-indigo-200' : 'text-gray-400'}`}
                aria-label={`Enviado às ${msg.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}`}
              >
                {msg.timestamp.toLocaleTimeString([], {
                  hour: '2-digit',
                  minute: '2-digit',
                })}
              </div>
            </div>
          </div>
        ))}

        {/* Indicador de "Digitando..." */}
        {isLoading && (
          <div
            className="flex justify-start animate-pulse"
            aria-label="Bot está digitando..."
          >
            <div className="bg-gray-200 p-3 rounded-lg rounded-bl-none text-xs text-gray-500 flex items-center gap-1">
              <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></span>
              <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-75"></span>
              <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-150"></span>
            </div>
          </div>
        )}

        {/* Elemento invisível usado como âncora para rolar até o fim */}
        <div ref={messagesEndRef} />
      </div>

      {/* Área de Input (Rodapé) */}
      <form
        onSubmit={handleSendMessage}
        className="p-4 bg-white border-t border-gray-100 flex gap-2 items-center"
      >
        <input
          ref={inputRef}
          type="text"
          className="flex-1 border border-gray-300 rounded-full px-4 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500 text-sm transition-shadow disabled:bg-gray-100 disabled:text-gray-500"
          placeholder="Digite sua dúvida aqui..."
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          disabled={isLoading} // Bloqueia input enquanto carrega
          aria-label="Digite sua mensagem"
        />
        <button
          type="submit"
          disabled={isLoading || !inputText.trim()}
          className="bg-indigo-600 text-white p-2 rounded-full hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors shadow-sm focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 focus:outline-none"
          title="Enviar Mensagem"
          aria-label="Enviar Mensagem"
        >
          {/* Ícone de Enviar (SVG) */}
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            strokeWidth={2}
            stroke="currentColor"
            className="w-5 h-5"
            aria-hidden="true"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M6 12L3.269 3.126A59.768 59.768 0 0121.485 12 59.77 59.77 0 013.27 20.876L5.999 12zm0 0h7.5"
            />
          </svg>
        </button>
      </form>
    </div>
  );
};

export default ChatWindow;
