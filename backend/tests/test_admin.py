# test_admin.py

import unittest
import sys
import os

# Adiciona o diretório pai ao path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import admin

class TestAdmin(unittest.TestCase):

    # ==========================================
    # 1. TESTES DE SUCESSO
    # ==========================================

    def test_login_success(self):
        """Testa se a senha exata retorna True."""
        self.assertTrue(admin.admin_login("1234"))

    # ==========================================
    # 2. TESTES DE FALHA (SENHA INCORRETA)
    # ==========================================

    def test_login_failure_wrong_content(self):
        """Testa senhas com conteúdo errado."""
        self.assertFalse(admin.admin_login("senha_errada"))
        self.assertFalse(admin.admin_login("12345")) # Superstring
        self.assertFalse(admin.admin_login("123"))   # Substring

    def test_login_failure_empty(self):
        """Testa string vazia."""
        self.assertFalse(admin.admin_login(""))

    def test_login_failure_whitespace(self):
        """Testa se espaços extras invalidam a senha (Trim)."""
        # A senha é '1234', então ' 1234 ' deve ser considerada errada
        # a menos que você adicione .strip() no código original.
        self.assertFalse(admin.admin_login(" 1234 "))
        self.assertFalse(admin.admin_login("1234 "))

    # ==========================================
    # 3. TESTES DE TIPAGEM E ROBUSTEZ
    # ==========================================

    def test_login_edge_case_integer(self):
        """Testa se passar o NÚMERO 1234 (int) falha."""
        # '1234' (str) != 1234 (int). O sistema não deve aceitar inteiros.
        self.assertFalse(admin.admin_login(1234)) # type: ignore

    def test_login_edge_case_none(self):
        """Testa se passar None falha sem quebrar o código."""
        # Se o código fosse `password.strip()`, isso quebraria.
        # Como é apenas `==`, deve retornar False suavemente.
        self.assertFalse(admin.admin_login(None)) # type: ignore

if __name__ == "__main__":
    unittest.main()