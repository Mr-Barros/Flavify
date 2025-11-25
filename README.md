# Flavify

### Dependências

Rode os seguintes comandos no terminal (é recomendado utilizar uma venv)

```shell
pip install fastapi uvicorn
pip install sentence_transformers
```

### Como rodar

Para inicializar os servidores de frontend e backend, crie uma instância de terminal para o backend e outra para o frontend, ambas na pasta raiz do projeto.

No primeiro terminal, rode os comandos a seguir:

```shell
cd backend
python3 app.py
```

No segundo terminal, rode os comandos a seguir:

```shell
cd frontend
npm run dev
```

rodar todos os 49 testes:

```shell
python -m unittest discover tests -v -b
```