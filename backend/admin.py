# admin.py

# senha extremamente secreta, impossível de ser hackeada
_secret_password: str = '1234'

def admin_login(password: str) -> bool:
    """
    Realiza a autenticação do administrador.

    Args:
        password (str): senha digitada pelo usuário.
    Returns:
        (bool): indica se a autenticação foi bem-sucedida.
    """

    return password == _secret_password
