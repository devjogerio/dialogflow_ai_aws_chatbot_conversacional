import ChatWindow from "../components/ChatWindow";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-4 bg-gray-100">
      <div className="w-full max-w-4xl">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-indigo-800 mb-2">Nexus AI</h1>
          <p className="text-gray-600">Seu assistente virtual para suporte técnico e orçamentos.</p>
        </div>
        <ChatWindow />
      </div>
    </main>
  );
}
