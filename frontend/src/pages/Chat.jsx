import { useState } from "react";
import axios from "axios";

export default function Chat() {
  const [question, setQuestion] = useState("");
  const [response, setResponse] = useState("");

  const askQuestion = async () => {
    try {
      const res = await axios.post("http://localhost:8000/chat/", {
        question: question,
      });

      setResponse(res.data.answer);
    } catch (err) {
      console.error(err);
      setResponse("Error connecting to backend");
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>AI Chat</h1>

      <input
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Ask something..."
      />

      <button onClick={askQuestion}>Ask</button>

      <p>{response}</p>
    </div>
  );
}