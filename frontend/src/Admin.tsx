import { useState, useEffect } from "react";
import { Trash2, Plus, Lock, KeyRound, Save, LogOut, Pencil, X, Check } from "lucide-react";

type Question = {
    question_id: string;
    statement: string;
    correct_answer: string;
};

export default function Admin() {
    // Estados de Autenticação
    const [token, setToken] = useState<string | null>(localStorage.getItem("admin_token"));
    const [password, setPassword] = useState("");
    
    // Estados de Dados
    const [questions, setQuestions] = useState<Question[]>([]);
    
    // Estados do Formulário de Criação
    const [newStatement, setNewStatement] = useState("");
    const [newAnswer, setNewAnswer] = useState("");
    const [isSubmitting, setIsSubmitting] = useState(false);

    const [editingId, setEditingId] = useState<string | null>(null);
    const [editStatement, setEditStatement] = useState("");
    const [editAnswer, setEditAnswer] = useState("");

    // Carregar questões ao entrar (se estiver logado)
    useEffect(() => {
        if (token) loadQuestions();
    }, [token]);

    async function handleLogin(e: React.FormEvent) {
        e.preventDefault();
        try {
            const res = await fetch("http://127.0.0.1:5000/admin/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ password }),
            });
            
            if (res.ok) {
                const data = await res.json();
                setToken(data.token);
                localStorage.setItem("admin_token", data.token);
            } else {
                alert("Senha incorreta!");
            }
        } catch (err) {
            console.error(err);
            alert("Erro ao conectar com o servidor");
        }
    }

    async function loadQuestions() {
        try {
            const res = await fetch("http://127.0.0.1:5000/questions");
            const data = await res.json();
            // O backend retorna um objeto {id: {...}}, transformamos em array
            setQuestions(Object.values(data));
        } catch (error) {
            console.error("Erro ao carregar questões", error);
        }
    }

    async function handleCreate(e: React.FormEvent) {
        e.preventDefault();
        if (!newStatement || !newAnswer) return;
        setIsSubmitting(true);

        try {
            await fetch("http://127.0.0.1:5000/questions", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ statement: newStatement, correct_answer: newAnswer }),
            });

            setNewStatement("");
            setNewAnswer("");
            loadQuestions(); // Recarrega a lista
        } catch (error) {
            console.error("Erro ao criar", error);
        } finally {
            setIsSubmitting(false);
        }
    }

    async function handleUpdate(id: string) {
        if (!editStatement || !editAnswer) return;

        try {
            await fetch(`http://127.0.0.1:5000/questions/${id}`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    statement: editStatement,
                    correct_answer: editAnswer
                })
            });

            setEditingId(null);
            loadQuestions();
        } catch (error) {
            console.error("Erro ao atualizar", error);
        }
    }

    async function handleDelete(id: string) {
        if (!confirm("Tem certeza que deseja deletar esta questão?")) return;
        
        try {
            await fetch(`http://127.0.0.1:5000/questions/${id}`, {
                method: "DELETE",
            });
            loadQuestions();
        } catch (error) {
            console.error("Erro ao deletar", error);
        }
    }

    function handleLogout() {
        setToken(null);
        localStorage.removeItem("admin_token");
        setPassword("");
    }

    // --- TELA DE LOGIN ---
    if (!token) {
        return (
            <div className="flex items-center justify-center min-h-[80vh] px-4">
                <form onSubmit={handleLogin} className="w-full max-w-md bg-gray-900 border border-gray-800 p-8 rounded-2xl shadow-2xl animate-in fade-in zoom-in duration-300">
                    <div className="flex justify-center mb-6">
                        <div className="p-4 bg-purple-500/10 rounded-full ring-1 ring-purple-500/50">
                            <Lock className="w-8 h-8 text-purple-500" />
                        </div>
                    </div>
                    <h2 className="text-2xl font-bold text-center text-white mb-2">Acesso Restrito</h2>
                    <p className="text-center text-gray-400 mb-8">Digite sua senha de administrador</p>
                    
                    <div className="space-y-4">
                        <div className="relative group">
                            <KeyRound className="absolute left-3 top-3.5 text-gray-500 group-focus-within:text-purple-400 transition-colors" size={20} />
                            <input
                                type="password"
                                placeholder="Senha (1234)"
                                className="w-full bg-gray-950 border border-gray-700 text-white pl-10 pr-4 py-3 rounded-xl focus:ring-2 focus:ring-purple-500/50 focus:border-purple-500 outline-none transition-all placeholder:text-gray-600"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                            />
                        </div>
                        <button className="w-full bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white font-bold py-3 rounded-xl transition-all shadow-lg shadow-purple-900/20 active:scale-95">
                            Entrar no Painel
                        </button>
                    </div>
                </form>
            </div>
        );
    }

    // --- TELA DO DASHBOARD ---
    return (
        <div className="pt-24 pb-12 max-w-5xl mx-auto px-4">
            {/* Cabeçalho */}
            <div className="flex justify-between items-end mb-8 border-b border-gray-800 pb-6">
                <div>
                    <h1 className="text-3xl font-bold text-white mb-1">Painel de Controle</h1>
                    <p className="text-gray-400 text-sm">Gerencie o banco de dados de conhecimento</p>
                </div>
                <button 
                    onClick={handleLogout} 
                    className="flex items-center gap-2 px-4 py-2 text-sm font-medium text-gray-400 hover:text-red-400 hover:bg-red-400/10 rounded-lg transition-colors"
                >
                    <LogOut size={16} /> Sair
                </button>
            </div>

            {/* Formulário de Criação */}
            <div className="bg-gray-900 border border-gray-800 rounded-2xl p-6 mb-10 shadow-xl">
                <h2 className="text-lg font-semibold text-purple-400 mb-6 flex items-center gap-2">
                    <div className="p-1.5 bg-purple-500/20 rounded-lg"><Plus size={18} /></div>
                    Adicionar Nova Questão
                </h2>
                
                <form onSubmit={handleCreate} className="space-y-5">
                    <div>
                        <label className="block text-xs font-medium text-gray-500 uppercase tracking-wider mb-2">Enunciado da Pergunta</label>
                        <input
                            type="text"
                            className="w-full bg-gray-950 border border-gray-700 rounded-xl p-3 text-white focus:border-purple-500 focus:ring-1 focus:ring-purple-500 outline-none transition-colors"
                            placeholder="Ex: Qual a velocidade da luz?"
                            value={newStatement}
                            onChange={e => setNewStatement(e.target.value)}
                        />
                    </div>
                    <div>
                        <label className="block text-xs font-medium text-gray-500 uppercase tracking-wider mb-2">Resposta Esperada (Gabarito)</label>
                        <textarea
                            className="w-full bg-gray-950 border border-gray-700 rounded-xl p-3 text-white focus:border-purple-500 focus:ring-1 focus:ring-purple-500 outline-none transition-colors h-24 resize-none"
                            placeholder="Ex: Aproximadamente 299.792.458 m/s..."
                            value={newAnswer}
                            onChange={e => setNewAnswer(e.target.value)}
                        />
                    </div>
                    <div className="flex justify-end">
                        <button 
                            disabled={isSubmitting || !newStatement || !newAnswer}
                            className="flex items-center gap-2 bg-white text-black hover:bg-gray-200 px-6 py-2.5 rounded-xl font-bold transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-lg shadow-white/10"
                        >
                            <Save size={18} /> 
                            {isSubmitting ? 'Salvando...' : 'Salvar Questão'}
                        </button>
                    </div>
                </form>
            </div>

            {/* Lista de Questões */}
            <div className="space-y-4">
                <div className="flex items-center justify-between mb-4">
                    <h2 className="text-xl font-bold text-white">Questões Ativas</h2>
                    <span className="bg-gray-800 text-gray-300 px-3 py-1 rounded-full text-xs font-bold border border-gray-700">
                        {questions.length} total
                    </span>
                </div>

                {questions.length === 0 ? (
                    <div className="text-center py-12 text-gray-500 border-2 border-dashed border-gray-800 rounded-xl">
                        Nenhuma questão cadastrada ainda.
                    </div>
                ) : (
                    <div className="grid gap-4">
                        {questions.map(q => (
                            <div 
                                key={q.question_id} 
                                className="bg-gray-900/40 border border-gray-800 p-5 rounded-xl group hover:border-gray-600 hover:bg-gray-900 transition-all"
                            >
                                {editingId === q.question_id ? (
                                    // --- FORMULÁRIO DE EDIÇÃO ---
                                    <div className="space-y-4">
                                        <input
                                            className="w-full bg-gray-950 border border-gray-700 rounded-xl p-3 text-white"
                                            value={editStatement}
                                            onChange={e => setEditStatement(e.target.value)}
                                        />

                                        <textarea
                                            className="w-full bg-gray-950 border border-gray-700 rounded-xl p-3 text-white h-24 resize-none"
                                            value={editAnswer}
                                            onChange={e => setEditAnswer(e.target.value)}
                                        />

                                        <div className="flex gap-3 justify-end">
                                            <button
                                                className="p-2 bg-gray-800 text-gray-300 rounded-lg hover:bg-gray-700"
                                                onClick={() => setEditingId(null)}
                                            >
                                                <X size={18} />
                                            </button>

                                            <button
                                                className="p-2 bg-green-600 text-white rounded-lg hover:bg-green-500"
                                                onClick={() => handleUpdate(q.question_id)}
                                            >
                                                <Check size={18} />
                                            </button>
                                        </div>
                                    </div>
                                ) : (
                                    // --- VISUALIZAÇÃO NORMAL ---
                                    <div className="flex justify-between items-start">
                                        <div className="space-y-2">
                                            <p className="font-medium text-lg text-gray-200">{q.statement}</p>
                                            <div className="flex items-center gap-2 text-sm text-gray-500">
                                                <span className="w-2 h-2 rounded-full bg-green-500/50"></span>
                                                Resposta: <span className="text-gray-400">{q.correct_answer}</span>
                                            </div>
                                        </div>

                                        <div className="flex gap-2 opacity-0 group-hover:opacity-100 transition-all">
                                            {/* Botão EDITAR */}
                                            <button
                                                onClick={() => {
                                                    setEditingId(q.question_id);
                                                    setEditStatement(q.statement);
                                                    setEditAnswer(q.correct_answer);
                                                }}
                                                className="p-2 text-gray-500 hover:text-blue-400 hover:bg-blue-500/10 rounded-lg transition"
                                                title="Editar Questão"
                                            >
                                                <Pencil size={18} />
                                            </button>

                                            {/* Botão DELETAR */}
                                            <button 
                                                onClick={() => handleDelete(q.question_id)}
                                                className="p-2 text-gray-500 hover:text-red-400 hover:bg-red-500/10 rounded-lg transition"
                                                title="Excluir Questão"
                                            >
                                                <Trash2 size={18} />
                                            </button>
                                        </div>
                                    </div>
                                )}
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
}