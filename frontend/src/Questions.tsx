import { useEffect, useState } from "react";
import { QuestionCard } from "./QuestionCard"; // <--- Agora esse import vai funcionar
import { Ghost } from 'lucide-react';

type Question = {
    question_id: string;
    statement: string;
};

type QuestionsResponse = {
    [id: string]: Question;
};

export default function Questions() {
    const [questions, setQuestions] = useState<Question[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        async function loadQuestions() {
            try {
                const response = await fetch("http://127.0.0.1:5000/questions");
                const data: QuestionsResponse = await response.json();
                // O backend retorna um dicionário, transformamos em array aqui
                setQuestions(Object.values(data));
            } catch (err) {
                console.error("Failed to load questions:", err);
            } finally {
                setLoading(false);
            }
        }
        loadQuestions();
    }, []);

    if (loading) {
        return (
            <div className="flex flex-col items-center justify-center min-h-[60vh] gap-4">
                <div className="w-10 h-10 border-4 border-purple-500/30 border-t-purple-500 rounded-full animate-spin" />
                <p className="text-gray-400 animate-pulse">Carregando desafios...</p>
            </div>
        );
    }

    return (
        <div className="pt-24 pb-12 max-w-6xl mx-auto px-4">
            <div className="mb-12 text-center">
                <h1 className="text-4xl md:text-5xl font-extrabold text-white mb-4 tracking-tight">
                    Desafie seu <span className="text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-indigo-400">Conhecimento</span>
                </h1>
                <p className="text-gray-400 text-lg max-w-2xl mx-auto">
                    Responda às questões abaixo e através de NLP, iremos analisar sua precisão semântica instantaneamente.
                </p>
            </div>

            {questions.length === 0 ? (
                <div className="text-center py-20 bg-gray-900/50 rounded-2xl border border-gray-800 border-dashed">
                    <Ghost size={48} className="mx-auto text-gray-600 mb-4" />
                    <p className="text-gray-400 text-lg">Nenhuma questão encontrada.</p>
                    <p className="text-gray-600 text-sm mt-2">Acesse o painel de administrador para criar algumas.</p>
                </div>
            ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {questions.map((question) => (
                        <QuestionCard 
                            key={question.question_id}
                            id={question.question_id}
                            statement={question.statement}
                        />
                    ))}
                </div>
            )}
        </div>
    );
}