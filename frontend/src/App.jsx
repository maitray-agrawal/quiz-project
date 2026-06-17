import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import Students from "./pages/Students";
import Chat from "./pages/Chat";

function App() {
  return (
    <BrowserRouter>
      <div>
        <nav style={{ padding: "10px", background: "black", color: "white" }}>
          <Link to="/" style={{ marginRight: "10px", color: "white" }}>
            Students
          </Link>
          <Link to="/chat" style={{ color: "white" }}>
            Chat
          </Link>
        </nav>

        <Routes>
          <Route path="/" element={<Students />} />
          <Route path="/chat" element={<Chat />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;