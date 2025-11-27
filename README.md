# Flavify

## Dependências

Rode os seguintes comandos no terminal para instalar todas as bibliotecas necessárias (Backend e Frontend).

**Backend:**
```shell
pip install fastapi
pip install uvicorn
pip install sentence_transformers
pip install httpx
```

**Frontend:**
```shell
cd frontend
npm install
npm install lucide-react
```
## Como rodar
Para inicializar os servidores de frontend e backend, crie uma instância de terminal para o backend e outra para o frontend, ambas na pasta raiz do projeto.

No primeiro terminal (Backend), rode os comandos a seguir:

```shell
cd backend
python app.py
```
(Se estiver no Linux/Mac, use python3 app.py)

No segundo terminal (Frontend), rode os comandos a seguir:

```shell
cd frontend
npm run dev
```

## Testes Automatizados
Para rodar a bateria completa de testes (49 testes cobrindo rotas, lógica, IA e validações):

```shell
cd backend
python -m unittest discover tests -v -b
```