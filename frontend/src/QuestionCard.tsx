import { useState } from 'react';
import { Send, CheckCircle2, AlertCircle, XCircle, MinusCircle } from 'lucide-react';

interface QuestionProps {
    id: string;
    statement: string;
}

export function QuestionCard({ id, statement }: QuestionProps) {
    const [answer, setAnswer] = useState('');
    const [score, setScore] = useState<number | null>(null);
    const [loading, setLoading] = useState(false);

    async function handleEvaluate() {
        if (!answer.trim()) return;
        setLoading(true);

        try {
            const response = await fetch(`http://127.0.0.1:5000/questions/evaluate/${id}`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ answer }),
            });
            const data = await response.json();
            setScore(data.score);
        } catch (err) {
            console.error(err);
        } finally {
            setLoading(false);
        }
    }

    // Define cor e ícone baseados na nota
    const getFeedback = (s: number) => {
        if (s === 100) return { color: 'text-green-400 bg-green-500/10 border-green-500/20', icon: <CheckCircle2 />, text: 'Perfeito!' };
        if (s >= 70) return { color: 'text-blue-400 bg-blue-500/10 border-blue-500/20', icon: <CheckCircle2 />, text: 'Muito bom!' };
        if (s >= 40) return { color: 'text-yellow-400 bg-yellow-500/10 border-yellow-500/20', icon: <MinusCircle />, text: 'Na média' };
        return { color: 'text-red-400 bg-red-500/10 border-red-500/20', icon: <XCircle />, text: 'Precisa melhorar' };
    };

    const feedback = score !== null ? getFeedback(score) : null;

    return (
        <div className="bg-gray-900 rounded-xl border border-gray-800 p-6 shadow-xl hover:border-purple-500/30 transition-all group">
            <h3 className="text-lg font-medium text-gray-100 mb-4 min-h-[3rem]">
                {statement}
            </h3>

            <div className="relative">
                <textarea
                    className="w-full bg-gray-950 border border-gray-700 rounded-lg p-3 text-sm text-gray-200 focus:outline-none focus:ring-2 focus:ring-purple-500/50 focus:border-purple-500 transition-all resize-none h-28 disabled:opacity-50"
                    placeholder="Sua resposta..."
                    value={answer}
                    onChange={(e) => setAnswer(e.target.value)}
                    disabled={score !== null || loading}
                />

                {score === null ? (
                    <button
                        onClick={handleEvaluate}
                        disabled={!answer.trim() || loading}
                        className="absolute bottom-3 right-3 bg-purple-600 hover:bg-purple-500 text-white p-2 rounded-lg transition-all shadow-lg disabled:opacity-50 disabled:cursor-not-allowed active:scale-95"
                    >
                        {loading ? (
                            <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                        ) : (
                            <Send size={18} />
                        )}
                    </button>
                ) : (
                    <div className={`mt-4 p-3 rounded-lg border flex items-center gap-3 ${feedback?.color} animate-in fade-in slide-in-from-top-2`}>
                        {feedback?.icon}
                        <div className="flex flex-col">
                            <span className="font-bold text-lg leading-none">{score}</span>
                            <span className="text-xs opacity-80 uppercase tracking-wider">{feedback?.text}</span>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}