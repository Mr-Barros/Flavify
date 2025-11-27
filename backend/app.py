# app.py

from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException

from question import (
    evaluate,
    create_question,
    get_all_questions,
    update_question,
    delete_question,
    save_questions_to_json,
    load_questions_from_json, 
)

from admin import admin_login

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gerenciador de ciclo de vida da aplicação, executando rotinas de inicialização
    e finalização, como carregar e salvar questões.

    Args:
        app (FastAPI): Instância do aplicativo FastAPI.

    ## Assertivas de saída:
        - O arquivo questions.json será carregado no início da aplicação (se existir).
        - As questões serão salvas no arquivo questions.json ao final da execução.
    """

    load_questions_from_json()
    yield
    save_questions_to_json()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/questions')
def api_get_all_questions() -> dict[str, dict[str, str]]:
    """
    Endpoint que retorna todas as questões cadastradas.

    Returns:
        (dict[str, dict[str, str]]): Dicionário contendo todas as questões registradas.

    ## Assertivas de saída:
        - Cada questão retornada possui campos question_id, statement e correct_answer.
        - O question_id de cada questão corresponde à chave do dicionário.
    """

    return get_all_questions()

@app.post('/questions')
def api_create_question(body: dict[str, str]) -> int:
    """
    Endpoint para criação de uma nova questão.

    Args:
        body (dict[str, str]): Dicionário contendo os campos:
            - statement (str): enunciado da questão.
            - correct_answer (str): gabarito da questão.

    Returns:
        (int): Código indicando o sucesso (1) ou falha (0) na criação.

    ## Assertivas de entrada:
        - Os campos statement e correct_answer devem ser strings não vazias.
    ## Assertivas de saída:
        - Retorna 1 em caso de sucesso e 0 em caso de falha.
    """

    statement = body.get('statement', '')
    correct_answer = body.get('correct_answer', '')
    return create_question(statement, correct_answer)

@app.put('/questions/{question_id}')
def api_update_question(question_id: str, body: dict[str, str]) -> int:
    """
    Endpoint para atualizar uma questão existente.

    Args:
        question_id (str): Identificador da questão.
        body (dict[str, str]): Dicionário contendo:
            - statement (str): novo enunciado.
            - correct_answer (str): novo gabarito.

    Returns:
        (int): Código indicando sucesso (1) ou falha (0).

    ## Assertivas de entrada:
        - question_id deve ser uma string correspondente a um UUID existente.
        - Os campos statement e correct_answer devem ser strings não vazias.
    ## Assertivas de saída:
        - Retorna 1 se atualização ocorrer com sucesso.
        - Retorna 0 se a questão não existir.
    """

    statement = body.get('statement', '')
    correct_answer = body.get('correct_answer', '')
    return update_question(question_id, statement, correct_answer)

@app.post('/questions/evaluate/{question_id}')
def api_evaluate(question_id: str, body: dict[str, str]) -> dict[str, int]:
    """
    Endpoint para avaliar a resposta de uma questão.

    Args:
        question_id (str): Identificador da questão.
        body (dict[str, str]): Dicionário contendo:
            - answer (str): resposta do usuário.

    Returns:
        (dict[str, int]): Objeto contendo o campo:
            - score (int): pontuação obtida.

    ## Assertivas de entrada:
        - question_id deve ser uma string correspondente a um UUID.
        - answer deve ser uma string não vazia.
    ## Assertivas de saída:
        - score pode ser 0, 40, 70, 100 ou -1 caso a questão não exista.
    """

    answer = body.get('answer', '')
    score = evaluate(question_id, answer)
    return {'score': score}

@app.delete('/questions/{question_id}')
def api_delete_question(question_id: str) -> int:
    """
    Endpoint para excluir uma questão cadastrada.

    Args:
        question_id (str): Identificador da questão a ser removida.

    Returns:
        (int): Código indicando sucesso (1) ou falha (0).

    ## Assertivas de entrada:
        - question_id deve ser uma string correspondente a um UUID.
    ## Assertivas de saída:
        - Retorna 1 se a questão for removida.
        - Retorna 0 caso a questão não exista.
    """

    return delete_question(question_id)

@app.post('/admin/login')
def api_admin_login(body: dict[str, str]) -> dict[str, str]:
    """
    Endpoint de login administrativo.

    Args:
        body (dict[str, str]): Dicionário contendo:
            - password (str): senha fornecida pelo usuário.

    Returns:
        (dict[str, str]): Objeto contendo o campo:
            - token (str): token de autenticação.

    ## Assertivas de entrada:
        - O campo password deve ser fornecido.
    ## Assertivas de saída:
        - Retorna um token fixo caso a senha esteja correta.
        - Retorna erro HTTP 401 se a senha for incorreta.
    """

    password = body.get('password', '')
    if not admin_login(password):
        raise HTTPException(
            status_code=401,
            detail="Senha incorreta."
        )
    
    return {"token": "admin-token-123"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000)
