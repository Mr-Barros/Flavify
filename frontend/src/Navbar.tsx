import { Link, useLocation } from "react-router-dom";
import { LayoutDashboard, ListTodo, Zap } from 'lucide-react';

export default function Navbar() {
    const location = useLocation();

    // Função auxiliar para estilizar os botões
    const getLinkClass = (path: string) => {
        const isActive = location.pathname === path;
        return `flex items-center gap-2 px-4 py-2 rounded-lg transition-all text-sm font-medium ${
            isActive 
                ? 'bg-purple-600 text-white shadow-lg shadow-purple-500/20' 
                : 'text-gray-400 hover:text-white hover:bg-gray-800'
        }`;
    };

    return (
        <nav className="fixed top-0 left-0 w-full bg-gray-950/80 backdrop-blur-md border-b border-gray-800 z-50">
            <div className="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
                
                {/* Logo */}
                <div className="flex items-center gap-2">
                    <div className="w-8 h-8 bg-gradient-to-tr from-purple-500 to-indigo-500 rounded-lg flex items-center justify-center text-white shadow-purple-500/20 shadow-lg">
                        <Zap size={20} fill="white" />
                    </div>
                    <span className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-purple-400 to-indigo-400">
                        Flavify
                    </span>
                </div>

                {/* Links de Navegação */}
                <div className="flex gap-2">
                    <Link to="/" className={getLinkClass('/')}>
                        <ListTodo size={18} />
                        Questões
                    </Link>
                    <Link to="/admin" className={getLinkClass('/admin')}>
                        <LayoutDashboard size={18} />
                        Administrador
                    </Link>
                </div>
            </div>
        </nav>
    );
}