#test_question.py

import unittest
from unittest.mock import patch, mock_open, Mock
import sys
import os
import json

# Adiciona o diretório pai (backend) ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import question

class TestQuestion(unittest.TestCase):

    def setUp(self):
        """Limpa o banco de dados em memória antes de cada teste."""
        question.questions.clear()

    # 1. TESTES DE CRIAÇÃO (CREATE)

    def test_create_question_success(self):
        """Criação padrão com dados válidos."""
        result = question.create_question("Qual a cor?", "Azul")
        self.assertEqual(result, 1)
        self.assertEqual(len(question.questions), 1)
        
        q_id = list(question.questions.keys())[0]
        self.assertEqual(question.questions[q_id]['statement'], "Qual a cor?")

    def test_create_question_empty_strings(self):
        """Criação com strings vazias (Limite)."""
        # O sistema permite criar questão sem texto? Sim. Vamos garantir que não quebra.
        result = question.create_question("", "")
        self.assertEqual(result, 1)
        
        q_id = list(question.questions.keys())[0]
        self.assertEqual(question.questions[q_id]['statement'], "")
        self.assertEqual(question.questions[q_id]['correct_answer'], "")

    # 2. TESTES DE LEITURA (GETTERS)

    def test_get_all_questions_copy(self):
        """Retorna cópia segura do dicionário."""
        question.create_question("Q1", "A1")
        all_q = question.get_all_questions()
        self.assertEqual(len(all_q), 1)
        self.assertNotEqual(id(all_q), id(question.questions))

    def test_get_statement_success(self):
        """Busca enunciado existente."""
        question.create_question("Teste?", "Sim")
        q_id = list(question.questions.keys())[0]
        self.assertEqual(question.get_statement(q_id), "Teste?")

    def test_get_statement_not_found_crash(self):
        """Busca enunciado de ID inexistente (Deve gerar KeyError)."""
        # Como a função get_statement não tem tratamento de erro (try/except),
        # o teste correto é verificar se ela LEVANTA o erro esperado.
        with self.assertRaises(KeyError):
            question.get_statement("id_fantasma")

    def test_get_correct_answer_success(self):
        """Busca gabarito existente."""
        question.create_question("Teste?", "Sim")
        q_id = list(question.questions.keys())[0]
        self.assertEqual(question.get_correct_answer(q_id), "Sim")

    def test_get_correct_answer_not_found_crash(self):
        """Busca gabarito de ID inexistente (Deve gerar KeyError)."""
        with self.assertRaises(KeyError):
            question.get_correct_answer("id_fantasma")

    # 3. TESTES DE AVALIAÇÃO (EVALUATE)

    @patch('question.sentence_similarity')
    def test_evaluate_not_found(self, mock_similarity: Mock):
        """Avaliar ID inexistente."""
        result = question.evaluate("id_inexistente", "Resposta")
        self.assertEqual(result, -1)
        mock_similarity.assert_not_called()

    @patch('question.sentence_similarity')
    def test_evaluate_scores(self, mock_similarity: Mock):
        """Testa todas as faixas de pontuação (0, 40, 70, 100)."""
        question.create_question("Q", "A")
        q_id = list(question.questions.keys())[0]

        scenarios = [
            (0.15, 0),   # Similaridade < 0.20
            (0.35, 40),  # 0.20 <= Similaridade < 0.40
            (0.65, 70),  # 0.40 <= Similaridade < 0.70
            (0.95, 100)  # Similaridade >= 0.70
        ]

        for sim_value, expected_score in scenarios:
            mock_similarity.return_value = sim_value
            score = question.evaluate(q_id, "Resposta")
            self.assertEqual(score, expected_score, f"Falha para similaridade {sim_value}")

    @patch('question.sentence_similarity')
    def test_evaluate_empty_answer(self, mock_similarity: Mock):
        """Avaliar resposta vazia."""
        mock_similarity.return_value = 0.0
        question.create_question("Q", "A")
        q_id = list(question.questions.keys())[0]
        
        score = question.evaluate(q_id, "")
        self.assertEqual(score, 0)

    # 4. TESTES DE ATUALIZAÇÃO (UPDATE)

    def test_update_question_success(self):
        """Update completo."""
        question.create_question("Velho", "Velha")
        q_id = list(question.questions.keys())[0]
        result = question.update_question(q_id, "Novo", "Nova")
        self.assertEqual(result, 1)
        self.assertEqual(question.questions[q_id]['statement'], "Novo")

    def test_update_question_empty_strings(self):
        """Update para strings vazias."""
        question.create_question("Velho", "Velha")
        q_id = list(question.questions.keys())[0]
        result = question.update_question(q_id, "", "")
        self.assertEqual(result, 1)
        self.assertEqual(question.questions[q_id]['statement'], "")

    def test_update_question_not_found(self):
        """Update em ID inexistente."""
        result = question.update_question("fake_id", "Novo", "Nova")
        self.assertEqual(result, 0)

    # 5. TESTES DE REMOÇÃO (DELETE)

    def test_delete_question_success(self):
        """Delete existente."""
        question.create_question("Q", "A")
        q_id = list(question.questions.keys())[0]
        result = question.delete_question(q_id)
        self.assertEqual(result, 1)
        self.assertEqual(len(question.questions), 0)

    def test_delete_question_not_found(self):
        """Delete inexistente."""
        result = question.delete_question("fake_id")
        self.assertEqual(result, 0)

    # 6. TESTES DE PERSISTÊNCIA (JSON)

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    def test_save_questions(self, mock_json_dump: Mock, mock_file: Mock):
        """Salvar no arquivo JSON."""
        question.create_question("Q", "A")
        question.save_questions_to_json()
        mock_file.assert_called_with('data/questions.json', 'w', encoding='utf-8')
        self.assertTrue(mock_json_dump.called)

    @patch('builtins.open', new_callable=mock_open, read_data='[{"question_id": "1", "statement": "A", "correct_answer": "B"}]')
    def test_load_questions_success(self, mock_file: Mock):
        """Carregar do arquivo JSON."""
        question.load_questions_from_json()
        self.assertIn("1", question.questions)

    @patch('builtins.open', side_effect=FileNotFoundError)
    def test_load_questions_file_not_found(self, mock_file: Mock):
        """Carregar sem arquivo (não deve quebrar)."""
        try:
            question.load_questions_from_json()
        except Exception:
            self.fail("Deveria tratar FileNotFoundError silenciosamente")

    @patch('builtins.open', new_callable=mock_open, read_data='INVALID JSON')
    def test_load_questions_corrupted_json(self, mock_file: Mock):
        """Carregar arquivo JSON corrompido (Deve gerar JSONDecodeError)."""
        # Seu código NÃO tem try/except para JSONDecodeError. 
        # O teste correto é verificar se o erro SOBE para quem chamou.
        with self.assertRaises(json.JSONDecodeError):
            question.load_questions_from_json()

if __name__ == '__main__':
    unittest.main()