// App.tsx

import { Routes, Route } from "react-router-dom";
import Questions from "./Questions";
import Admin from "./Admin";
import Navbar from "./Navbar";

export default function App() {
    return (
        <>
            <Navbar />

            <Routes>
                <Route path="/" element={<Questions />} />
                <Route path="/admin" element={<Admin />} />
            </Routes>
        </>
        
    );
}
