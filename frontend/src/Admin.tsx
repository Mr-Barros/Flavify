
import { useState } from "react";

const API_URL = "http://127.0.0.1:5000";

type Question = {
    question_id: string;
    statement: string;
    correct_answer: string;
};

export default function Admin() {
    const [password, setPassword] = useState("");
    const [token, setToken] = useState<string | null>(null);

    const [questions, setQuestions] = useState<Question[]>([]);
    const [loading, setLoading] = useState(false);

    const [statement, setStatement] = useState("");
    const [correctAnswer, setCorrectAnswer] = useState("");
    const [editingId, setEditingId] = useState<string | null>(null);

    // Fetch all questions
    async function loadQuestions() {
        setLoading(true);
        const res = await fetch(`${API_URL}/questions`);
        const data = await res.json();
        setQuestions(Object.values(data));
        setLoading(false);
    }

    // Login function
    async function login() {
        const res = await fetch(`${API_URL}/admin/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ password }),
        });

        if (!res.ok) {
            alert("Senha incorreta");
            return;
        }

        const data = await res.json();
        setToken(data.token);
        loadQuestions();
    }

    // Create or update question
    async function saveQuestion() {
        if (!statement.trim() || !correctAnswer.trim()) {
            alert("Preencha todos os campos");
            return;
        }

        if (editingId) {
            // Update
            await fetch(`${API_URL}/questions/${editingId}`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    statement,
                    correct_answer: correctAnswer
                }),
            });
        } else {
            // Create
            await fetch(`${API_URL}/questions`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    statement,
                    correct_answer: correctAnswer
                }),
            });
        }

        setStatement("");
        setCorrectAnswer("");
        setEditingId(null);
        loadQuestions();
    }

    async function deleteQuestion(id: string) {
        if (!confirm("Tem certeza que deseja excluir?")) return;

        await fetch(`${API_URL}/questions/${id}`, {
            method: "DELETE"
        });
        loadQuestions();
    }

    // Prefill form for editing
    function startEditing(q: Question) {
        setEditingId(q.question_id);
        setStatement(q.statement);
        setCorrectAnswer(q.correct_answer);
    }

    // ============================
    // LOGIN SCREEN
    // ============================

    if (!token) {
        return (
            <div style={{ maxWidth: 400, margin: "50px auto" }}>
                <h1>Painel do Administrador</h1>
                <input
                    type="password"
                    placeholder="Senha"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    style={{ width: "100%", padding: 10 }}
                />
                <button
                    onClick={login}
                    style={{ marginTop: 10, width: "100%", padding: 10 }}
                >
                    Entrar
                </button>
            </div>
        );
    }

    // ============================
    // CRUD SCREEN
    // ============================

    return (
        <div style={{ maxWidth: 800, margin: "40px auto" }}>
            <h1>Gerenciar Questões</h1>

            <h2>{editingId ? "Editar Questão" : "Criar Nova Questão"}</h2>

            <input
                placeholder="Enunciado"
                value={statement}
                onChange={(e) => setStatement(e.target.value)}
                style={{ width: "100%", padding: 10, marginBottom: 10 }}
            />

            <textarea
                placeholder="Resposta correta"
                value={correctAnswer}
                onChange={(e) => setCorrectAnswer(e.target.value)}
                style={{ width: "100%", padding: 10, height: 100 }}
            />

            <button
                onClick={saveQuestion}
                style={{ marginTop: 10, padding: 10, width: "100%" }}
            >
                {editingId ? "Salvar Alterações" : "Criar Questão"}
            </button>

            {editingId && (
                <button
                    onClick={() => {
                        setEditingId(null);
                        setStatement("");
                        setCorrectAnswer("");
                    }}
                    style={{
                        marginTop: 10,
                        padding: 10,
                        width: "100%",
                        backgroundColor: "#777",
                    }}
                >
                    Cancelar Edição
                </button>
            )}

            <hr style={{ margin: "40px 0" }} />

            <h2>Lista de Questões</h2>

            {loading ? (
                <p>Carregando...</p>
            ) : (
                <ul>
                    {questions.map((q) => (
                        <li
                            key={q.question_id}
                            style={{
                                border: "1px solid #444",
                                padding: 15,
                                marginBottom: 10,
                                borderRadius: 8,
                            }}
                        >
                            <strong>{q.statement}</strong>
                            <p><em>Resposta correta:</em> {q.correct_answer}</p>

                            <button onClick={() => startEditing(q)}>
                                Editar
                            </button>

                            <button
                                onClick={() => deleteQuestion(q.question_id)}
                                style={{ marginLeft: 10, backgroundColor: "red", color: "white" }}
                            >
                                Excluir
                            </button>
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
}
