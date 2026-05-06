import { useState, useRef, useEffect } from "react";
import ReactMarkdown from "react-markdown";

export default function App() {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const chatRef = useRef(null);

  const API_URL = import.meta.env.VITE_API_URL;

  useEffect(() => {
    chatRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendQuery = async () => {
    if (!query.trim()) return;

    setMessages((prev) => [...prev, { role: "user", text: query }]);
    setQuery("");
    setLoading(true);

    setMessages((prev) => [...prev, { role: "bot", text: "" }]);

    try {
      const response = await fetch(`${API_URL}/query-stream`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
      });

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      let fullText = "";
      let done = false;

      while (!done) {
        const { value, done: doneReading } = await reader.read();
        done = doneReading;

        fullText += decoder.decode(value || new Uint8Array());

        setMessages((prev) => {
          const updated = [...prev];
          updated[updated.length - 1].text = fullText;
          return updated;
        });
      }
    } catch (err) {
      console.error(err);
    }

    setLoading(false);
  };

  return (
    <div className="h-screen flex flex-col text-gray-100 bg-linear-to-br from-gray-950 via-gray-900 to-black">

      {/* HEADER */}
      <header className="border-b border-white/10 backdrop-blur bg-black/30">
        <div className="max-w-4xl mx-auto px-4 py-4 flex items-center gap-2">
          <span className="text-xl">🚀</span>
          <h1 className="text-lg font-semibold tracking-tight">
            DecideAI
          </h1>
        </div>
      </header>

      {/* CHAT */}
      <main className="flex-1 overflow-y-auto px-4 py-8">
        <div className="max-w-4xl mx-auto space-y-8">

          {messages.length === 0 && (
            <div className="text-center text-gray-500 mt-32 text-sm">
              Ask a decision-based question
            </div>
          )}

          {messages.map((m, i) => (
            <div
              key={i}
              className={`flex ${
                m.role === "user" ? "justify-end" : "justify-start"
              }`}
            >
              <div
                className={`max-w-[75%] px-6 py-5 rounded-2xl backdrop-blur ${
                  m.role === "user"
                    ? "bg-blue-600 text-white"
                    : "bg-white/5 border border-white/10"
                }`}
              >
                <div className="prose prose-invert max-w-none text-sm leading-relaxed">
                  <ReactMarkdown>{m.text}</ReactMarkdown>
                </div>

                {i === messages.length - 1 && loading && (
                  <span className="animate-pulse ml-1">▍</span>
                )}
              </div>
            </div>
          ))}

          <div ref={chatRef} />
        </div>
      </main>

      {/* INPUT */}
      <footer className="border-t border-white/10 backdrop-blur bg-black/30">
        <div className="max-w-4xl mx-auto px-4 py-4 flex gap-3">

          <input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && sendQuery()}
            placeholder="Ask a question..."
            className="flex-1 bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 placeholder:text-gray-500"
          />

          <button
            onClick={sendQuery}
            className="bg-blue-600 hover:bg-blue-700 px-6 rounded-xl text-sm font-medium transition"
          >
            Send
          </button>
        </div>
      </footer>
    </div>
  );
}