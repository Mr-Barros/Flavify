# question.py

import json
from uuid import uuid4
from natural_language import sentence_similarity

# Encapsulamento dos atributos e disponibilização apenas das funções de acesso
__all__ = ["evaluate", "get_statement", "get_correct_answer", "create_question", 
           "get_all_questions", "update_question", "delete_question"]

questions: dict[str, dict[str, str]] = {}
"""
Formato de um dicionário de questão:
    question_id: str
    statement: str
    correct_answer: str
"""


def evaluate(question_id: str, answer: str) -> int:
    """
    Avalia a resposta dada à questão, chamando a função sentence_similarity do
    módulo natural_language.

    Args:
        question_id (str): Identificador da questão.
        answer(str): Resposta dada pelo usuário.
    Returns:
        (int): Valor que representa a pontuação obtida na questão.

    ## Assertivas de entrada:
        - O parâmetro question_id deve ser uma string única, correspondente a um UUID.
        - O parâmetro answer não deve ser uma string vazia.
    ## Assertivas de saída:
        - A saída pode ter os valores 0, 40, 70 ou 100. 
        - Caso a questão não seja encontrada, retorna um código de erro (-1).
    """

    if question_id not in questions:
        print(f"⚠️ Questão {question_id} não encontrada")
        return -1

    question = questions[question_id]
    similarity = sentence_similarity(answer, question['correct_answer'])

    if similarity < 0.20:
        return 0
    if similarity < 0.40:
        return 40
    if similarity < 0.70:
        return 70
    return 100


def get_statement(question_id: str) -> str:
    """
    Retorna o enunciado da questão referenciada.

    Args:
        question_id (str): Identificador da questão.
    Returns:
        (str): O enunciado da questão.

    ## Assertivas de entrada:
        - O parâmetro question_id deve ser uma string única, correspondente a um UUID.
    ## Assertivas de saída:
        - A string de saída não estará vazia.
    """
    question = questions[question_id]
    return question['statement']


def get_correct_answer(question_id: str) -> str:
    """
    Retorna o gabarito da questão referenciada.

    Args:
        question_id (str): Identificador da questão.
    Returns:
        (str): O gabarito da questão.

    ## Assertivas de entrada:
        - O parâmetro question_id deve ser uma string única, correspondente a um UUID.
    ## Assertivas de saída:
        - A string de saída não estará vazia.
    """
    question = questions[question_id]
    return question['correct_answer']


def create_question(statement: str, correct_answer: str) -> int:
    """
    Cria uma nova questão e a adiciona ao dicionário de questões.

    Args:
        statement (str): Enunciado da questão.
        correct_answer (str): Gabarito da questão.
    Returns:
        (int): Um inteiro indicando o status da operação.

    ## Assertivas de entrada:
        - Os parâmetros statement e correct_answer não devem ser strings vazias.
    ## Assertivas de saída:
        - Retorna 1 em caso de sucesso e 0 em caso de falha.
    """
    
    question_id: str = str(uuid4())
    questions[question_id] = {
        'question_id': question_id,
        'statement': statement,
        'correct_answer': correct_answer
    }

    print(f"✅ Questão {question_id} criada com sucesso")
    return 1


def get_all_questions() -> dict[str, dict[str, str]]:
    """
    Retorna todas as questões cadastradas no dicionário de questões.

    Returns:
        (dict[str, dict[str, str]]): Dicionário contendo todas as questões registradas, 
        identificadas por uma string question_id.

    ## Assertivas de saída:
        - Cada questão é um dicionário contendo os campos question_id, statement e correct_answer, todos strings.
        - O question_id da questão será igual à chave que a identifica.
    """
    return questions.copy()


def update_question(question_id: str, new_statement: str, new_correct_answer: str) -> int:
    """
    Atualiza os dados de uma questão existente no dicionário de questões.

    Args:
        question_id (str): Identificador da questão a ser atualizada.
        new_statement (str): Novo enunciado da questão.
        new_correct_answer (str): Novo gabarito da questão.
    Returns:
        (int): Valor indicando o status da operação. Retorna 1 em caso de sucesso e 0
        em caso de falha (por exemplo, se a questão não for encontrada).

    ## Assertivas de entrada:
        - O parâmetro question_id deve ser uma string única, correspondente a um UUID.
        - Os parâmetros new_statement e new_correct_answer não devem ser strings vazias.
    ## Assertivas de saída:
        - Retorna 1 em caso de sucesso e 0 em caso de falha.
    """

    if question_id not in questions:
        print(f"⚠️ Questão {question_id} não encontrada")
        return 0
    
    questions[question_id]['statement'] = new_statement
    questions[question_id]['correct_answer'] = new_correct_answer

    print(f"✅ Questão {question_id} atualizada com sucesso")
    return 1


def delete_question(question_id: str) -> int:
    """
    Remove uma questão existente do dicionário de questões.

    Args:
        question_id (str): Identificador da questão a ser removida.
    Returns:
        (int) Valor indicando o status da operação. Retorna 1 em caso de sucesso e 0
        em caso de falha (por exemplo, se a questão não for encontrada).

    ## Assertivas de entrada:
        - O parâmetro question_id deve ser uma string única, correspondente a um UUID.
    ## Assertivas de saída:
        - Retorna 1 em caso de sucesso e 0 em caso de falha.
    """

    if question_id not in questions:
        print(f"⚠️ Questão {question_id} não encontrada")
        return 0
    
    del questions[question_id]

    print(f"✅ Questão {question_id} removida com sucesso")
    return 1


def save_questions_to_json():
    """
    Salva o dicionário de questões no arquivo questions.json.

    ## Assertivas de saída:
        - As questões do dicionário serão salvas no arquivo questions.json.
    """
    question_list = list(questions.values())
    with open('data/questions.json', 'w', encoding='utf-8') as f:
        json.dump(question_list, f, indent=4, ensure_ascii=False)
    print("✅ Questões salvas em questions.json")


def load_questions_from_json():
    """
    Preenche o dicionário de questões com os dados do arquivo questions.json.

    ## Assertivas de saída:
        - O dicionário questions será preenchido com os dados do arquivo questions.json (se existir).
    """
    try:
        with open('data/questions.json', 'r', encoding='utf-8') as f:
            question_list = json.load(f)
            for question in question_list:
                question_id = question['question_id']
                questions[question_id] = question
            print("✅ Questões carregadas com sucesso")
    except FileNotFoundError:
        print("⚠️ Falha ao carregar as questões: questions.json não encontrado")