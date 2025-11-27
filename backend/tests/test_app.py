#test_app.py

import unittest
from unittest.mock import patch, Mock
from fastapi.testclient import TestClient
from typing import Any
import sys
import os

# Adiciona o diretório pai ao path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
import question 

client = TestClient(app)

class TestApp(unittest.TestCase):

    def setUp(self):
        """Limpa o banco de dados em memória antes de cada teste."""
        question.questions.clear()

    # ==========================================
    # 1. TESTES DE AUTENTICAÇÃO (ADMIN)
    # ==========================================

    def test_admin_login_success(self):
        """Login com senha correta."""
        payload = {"password": "1234"}
        response = client.post("/admin/login", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.json())

    def test_admin_login_wrong_password(self):
        """Login com senha errada."""
        payload = {"password": "senha_errada"}
        response = client.post("/admin/login", json=payload)
        self.assertEqual(response.status_code, 401)

    def test_admin_login_empty_body(self):
        """Login sem enviar senha (JSON vazio)."""
        # O código faz: password = body.get('password', '')
        # Então se mandar vazio, a senha vira "", que é incorreta. Deve dar 401.
        payload = {}
        response = client.post("/admin/login", json=payload)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()['detail'], "Senha incorreta.")

    # ==========================================
    # 2. TESTES DE CRIAÇÃO (POST /questions)
    # ==========================================

    def test_create_question_full(self):
        """Criação com todos os dados."""
        payload = {"statement": "Pergunta?", "correct_answer": "Resposta"}
        response = client.post("/questions", json=payload)
        self.assertEqual(response.status_code, 200)
        
        # Verifica se salvou corretamente
        q = list(question.questions.values())[0]
        self.assertEqual(q['statement'], "Pergunta?")
        self.assertEqual(q['correct_answer'], "Resposta")

    def test_create_question_partial(self):
        """Criação faltando dados (só enunciado)."""
        # O código define padrão '' para o que falta
        payload = {"statement": "Só pergunta"} 
        response = client.post("/questions", json=payload)
        self.assertEqual(response.status_code, 200)

        q = list(question.questions.values())[0]
        self.assertEqual(q['statement'], "Só pergunta")
        self.assertEqual(q['correct_answer'], "") # Deve estar vazio

    def test_create_question_empty(self):
        """Criação com body vazio."""
        payload = {}
        response = client.post("/questions", json=payload)
        self.assertEqual(response.status_code, 200)

        q = list(question.questions.values())[0]
        self.assertEqual(q['statement'], "")
        self.assertEqual(q['correct_answer'], "")

    # ==========================================
    # 3. TESTES DE LEITURA (GET /questions)
    # ==========================================

    def test_get_all_questions(self):
        """Busca todas as questões."""
        question.create_question("Q1", "A1")
        response = client.get("/questions")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    # ==========================================
    # 4. TESTES DE UPDATE (PUT /questions/{id})
    # ==========================================

    def test_update_question_success(self):
        """Update completo em ID existente."""
        question.create_question("Antigo", "Antigo")
        q_id = list(question.questions.keys())[0]

        payload = {"statement": "Novo", "correct_answer": "Novo"}
        response = client.put(f"/questions/{q_id}", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(question.questions[q_id]['statement'], "Novo")

    def test_update_question_partial(self):
        """Update parcial (enviando só enunciado)."""
        question.create_question("Antigo", "Antigo")
        q_id = list(question.questions.keys())[0]

        # Envia só statement, correct_answer deve virar "" pelo seu código .get(..., '')
        payload = {"statement": "Novo"}
        response = client.put(f"/questions/{q_id}", json=payload)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(question.questions[q_id]['statement'], "Novo")
        self.assertEqual(question.questions[q_id]['correct_answer'], "")

    def test_update_question_not_found(self):
        """Update em ID inexistente."""
        payload = {"statement": "Novo", "correct_answer": "Novo"}
        response = client.put("/questions/id_falso", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 0) # Retorna 0 (falha)

    # ==========================================
    # 5. TESTES DE DELETE (DELETE /questions/{id})
    # ==========================================

    def test_delete_question_success(self):
        """Delete em ID existente."""
        question.create_question("Q", "A")
        q_id = list(question.questions.keys())[0]
        response = client.delete(f"/questions/{q_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 1)

    def test_delete_question_not_found(self):
        """Delete em ID inexistente."""
        response = client.delete("/questions/id_falso")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 0)

    # ==========================================
    # 6. TESTES DE AVALIAÇÃO (POST /evaluate)
    # ==========================================

    @patch('app.evaluate')
    def test_evaluate_success(self, mock_evaluate: Mock):
        """Avaliação normal."""
        mock_evaluate.return_value = 100
        response = client.post("/questions/evaluate/qualquer_id", json={"answer": "resp"})
        self.assertEqual(response.json(), {'score': 100})

    @patch('app.evaluate')
    def test_evaluate_empty_answer(self, mock_evaluate: Mock):
        """Avaliação enviando resposta vazia ou json vazio."""
        mock_evaluate.return_value = 0
        
        # Teste enviando vazio
        response = client.post("/questions/evaluate/qualquer_id", json={})
        
        # O mock deve ser chamado com "" no segundo argumento
        mock_evaluate.assert_called_with("qualquer_id", "")
        self.assertEqual(response.json(), {'score': 0})

    @patch('app.evaluate')
    def test_evaluate_id_not_found(self, mock_evaluate: Mock):
        """Avaliação em ID inexistente."""
        mock_evaluate.return_value = -1
        response = client.post("/questions/evaluate/id_falso", json={"answer": "resp"})
        self.assertEqual(response.json(), {'score': -1})

    # ==========================================
    # 7. NOVOS TESTES: VALIDAÇÃO E PROTOCOLO (GAP FILLERS)
    # ==========================================

    def test_validation_invalid_types(self):
        """
        Tenta enviar uma LISTA onde deveria ser TEXTO.
        O FastAPI (Pydantic) deve bloquear com 422 Unprocessable Entity,
        pois sua API espera dict[str, str] e uma lista não pode ser convertida para string simples.
        """
        payload: dict[str, Any] = {"statement": ["isso", "é", "uma", "lista"], "correct_answer": "Ok"}
        response = client.post("/questions", json=payload)
        self.assertEqual(response.status_code, 422)

    def test_validation_malformed_json(self):
        """
        Envia um JSON quebrado (sintaxe inválida).
        Simula um cliente enviando bytes corrompidos.
        """
        response = client.post(
            "/questions", 
            content=b'{ "statement": "quebrado"', # Faltou fechar a chave
            headers={"Content-Type": "application/json"}
        )
        # O servidor deve reclamar que não conseguiu ler o JSON (400 ou 422 dependendo da versão)
        self.assertIn(response.status_code, [400, 422])

    def test_protocol_method_not_allowed(self):
        """
        Tenta usar DELETE na rota /questions (que só aceita GET e POST).
        Isso garante que ninguém apague o banco inteiro por engano.
        Deve retornar 405 Method Not Allowed.
        """
        response = client.delete("/questions")
        self.assertEqual(response.status_code, 405)

if __name__ == "__main__":
    unittest.main()