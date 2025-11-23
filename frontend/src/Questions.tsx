// Questions.tsx

import { useEffect, useState } from "react";

type Question = {
    question_id: string;
    statement: string;
};

type QuestionsResponse = {
    [id: string]: Question;
};

export default function Questions() {
    const [questions, setQuestions] = useState<Question[]>([]);
    const [answers, setAnswers] = useState<Record<string, string>>({});
    const [scores, setScores] = useState<Record<string, number>>({});
    const [loading, setLoading] = useState(true);

    // Load questions from backend
    useEffect(() => {
        async function loadQuestions() {
            try {
                const response = await fetch("http://127.0.0.1:5000/questions");
                const data: QuestionsResponse = await response.json();

                const questionList = Object.values(data);
                setQuestions(questionList);

                // Initialize empty answers
                const initialAnswers: Record<string, string> = {};
                questionList.forEach((q) => {
                    initialAnswers[q.question_id] = "";
                });
                setAnswers(initialAnswers);
            } catch (err) {
                console.error("Failed to load questions:", err);
            } finally {
                setLoading(false);
            }
        }

        loadQuestions();
    }, []);

    // Handle textfield input
    function handleAnswerChange(id: string, value: string) {
        setAnswers((prev) => ({ ...prev, [id]: value }));
    }

    // Submit answer to backend
    async function submitAnswer(id: string) {
        const userAnswer = answers[id];

        try {
            const response = await fetch(`http://127.0.0.1:5000/questions/evaluate/${id}`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ answer: userAnswer }),
            });

            const data = await response.json();
            setScores((prev) => ({ ...prev, [id]: data.score }));
        } catch (err) {
            console.error("Evaluation error:", err);
        }
    }

    if (loading) {
        return <p>Carregando questões...</p>;
    }

    return (
        <div style={{ padding: "30px", fontFamily: "Arial" }}>
        <h1>Flavify</h1>

        {questions.length === 0 && <p>Nenhuma questão encontrada.</p>}

        {questions.map((question) => (
            <div
                key={question.question_id}
                style={{
                    border: "1px solid #ccc",
                    borderRadius: "8px",
                    padding: "20px",
                    marginBottom: "20px",
                }}
            >
            <p style={{ fontWeight: "bold" }}>{question.statement}</p>

            <input
                type="text"
                placeholder="Your answer..."
                value={answers[question.question_id]}
                onChange={(e) => handleAnswerChange(question.question_id, e.target.value)}
                style={{
                    width: "100%",
                    padding: "8px",
                    marginTop: "10px",
                    marginBottom: "10px",
                    borderRadius: "4px",
                    border: "1px solid #999",
                }}
            />

            <button
                onClick={() => submitAnswer(question.question_id)}
                style={{
                    padding: "8px 16px",
                    border: "none",
                    borderRadius: "4px",
                    backgroundColor: "#007bff",
                    color: "white",
                    cursor: "pointer",
                }}
            >
                Enviar
            </button>

            {scores[question.question_id] !== undefined && (
                <p style={{ marginTop: "10px" }}>
                    Score: <strong>{scores[question.question_id]}</strong>
                </p>
            )}
            </div>
        ))}

        </div>
    );
}
