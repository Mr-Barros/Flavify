import { Routes, Route } from "react-router-dom";
import Navbar from "./Navbar";
import Questions from "./Questions";
import Admin from "./Admin";

function App() {
  return (
    <div className="min-h-screen bg-gray-950 text-gray-100 font-sans selection:bg-purple-500/30">
      <Navbar />
      
      {/* O Navbar é fixo, então precisamos desse padding-top para o conteúdo não ficar escondido atrás dele */}
      <main className="w-full">
        <Routes>
          <Route path="/" element={<Questions />} />
          <Route path="/admin" element={<Admin />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;