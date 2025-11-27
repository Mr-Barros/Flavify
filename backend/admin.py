# admin.py

# senha extremamente secreta, impossível de ser hackeada
_secret_password: str = '1234'

def admin_login(password: str) -> bool:
    """
    Realiza a autenticação do administrador.

    Args:
        password (str): Senha digitada pelo usuário.
    Returns:
        (bool): Indica se a autenticação foi bem-sucedida.

    ## Assertivas de entrada:
        - O parâmetro password não deve ser uma string vazia.
    ## Assertivas de saída:
        - Retorna true se password é a senha correta, e false caso contrário.
    """

    return password == _secret_password
