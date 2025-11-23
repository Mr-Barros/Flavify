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
    Gerenciador de ciclo de vida da aplicação para eventos de inicialização e término.
    
    Args:
        app (FastAPI): instância do aplicativo
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
def api_get_all_questions():
    return get_all_questions()


@app.post('/questions')
def api_create_question(body: dict[str, str]):
    statement = body.get('statement', '')
    correct_answer = body.get('correct_answer', '')
    return create_question(statement, correct_answer)


@app.put('/questions/{question_id}')
def api_update_question(question_id: str, body: dict[str, str]):
    statement = body.get('statement', '')
    correct_answer = body.get('correct_answer', '')
    return update_question(question_id, statement, correct_answer)


@app.post('/questions/evaluate/{question_id}')
def api_evaluate(question_id: str, body: dict[str, str]):
    answer = body.get('answer', '')
    score = evaluate(question_id, answer)
    return {'score': score}


@app.delete('/questions/{question_id}')
def api_delete_question(question_id: str):
    return delete_question(question_id)


@app.post('/admin/login')
def api_admin_login(body: dict[str, str]):
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
