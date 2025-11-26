# test_natural_language.py

import unittest
from unittest.mock import patch, MagicMock, Mock
import sys
import os

# Adiciona o diretório pai ao path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import natural_language

class TestSentenceSimilarity(unittest.TestCase):

    # ==========================================
    # 1. TESTES DE SUCESSO (HAPPY PATH)
    # ==========================================

    @patch('natural_language.util.cos_sim')
    @patch('natural_language.SentenceTransformer')
    def test_similarity_high(self, mock_transformer_class: Mock, mock_cos_sim: Mock):
        """Testa similaridade alta (0.95)."""
        mock_model_instance = mock_transformer_class.return_value
        mock_model_instance.encode.return_value = MagicMock()
        mock_cos_sim.return_value.item.return_value = 0.95

        result = natural_language.sentence_similarity("Oi", "Olá")

        self.assertEqual(result, 0.95)
        mock_transformer_class.assert_called_with("paraphrase-multilingual-MiniLM-L12-v2")

    @patch('natural_language.util.cos_sim')
    @patch('natural_language.SentenceTransformer')
    def test_similarity_low(self, mock_transformer_class: Mock, mock_cos_sim: Mock):
        """Testa similaridade baixa (0.10)."""
        mock_model_instance = mock_transformer_class.return_value
        mock_model_instance.encode.return_value = MagicMock()
        mock_cos_sim.return_value.item.return_value = 0.10

        result = natural_language.sentence_similarity("Batata", "Astronomia")

        self.assertEqual(result, 0.10)

    # ==========================================
    # 2. TESTES DE LÓGICA INTERNA (MATH & CLEANUP)
    # ==========================================

    @patch('natural_language.util.cos_sim')
    @patch('natural_language.SentenceTransformer')
    def test_similarity_negative_handling(self, mock_transformer_class: Mock, mock_cos_sim: Mock):
        """Testa proteção contra similaridade negativa (Math)."""
        # mock_model_instance = mock_transformer_class.return_value
        # Simula similaridade de -0.5
        mock_cos_sim.return_value.item.return_value = -0.5

        result = natural_language.sentence_similarity("A", "B")

        # Deve retornar 0 por causa do max(similarity, 0)
        self.assertEqual(result, 0)

    @patch('natural_language.util.cos_sim')
    @patch('natural_language.SentenceTransformer')
    def test_empty_strings(self, mock_transformer_class: Mock, mock_cos_sim: Mock):
        """Testa input de strings vazias."""
        mock_cos_sim.return_value.item.return_value = 0.0
        result = natural_language.sentence_similarity("", "")
        self.assertEqual(result, 0.0)

    # ==========================================
    # 3. TESTES DE FALHA E ERROS (CRASHES)
    # ==========================================

    @patch('natural_language.SentenceTransformer')
    def test_model_load_failure(self, mock_transformer_class: Mock):
        """Testa falha ao carregar o modelo de IA (Ex: Sem internet)."""
        # Simulamos que ao tentar iniciar a classe, ocorre um erro de Runtime
        mock_transformer_class.side_effect = RuntimeError("Falha ao baixar modelo")

        # Como seu código não tem try/except, ele DEVE repassar o erro.
        # Testamos se o erro realmente acontece.
        with self.assertRaises(RuntimeError):
            natural_language.sentence_similarity("A", "B")

    @patch('natural_language.SentenceTransformer')
    def test_encode_failure(self, mock_transformer_class: Mock):
        """Testa falha durante o processamento do texto (Encode)."""
        mock_instance = mock_transformer_class.return_value
        # Simulamos que o método .encode falhou
        mock_instance.encode.side_effect = Exception("Erro interno do PyTorch")

        with self.assertRaises(Exception):
            natural_language.sentence_similarity("A", "B")

if __name__ == "__main__":
    unittest.main()