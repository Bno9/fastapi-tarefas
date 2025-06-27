#1 importar tudo
#2 criar o "banco de dados (ainda é um dicionario)"
#3 criar as rotas POST (adicionar tarefa),PUT (atualizar tarefa (conclusao, nome, descrição)),GET (listar tarefa),DELETE (remover tarefa)
#4 testar

from pydantic import BaseModel
from fastapi import FastAPI, HTTPException

app = FastAPI()

DB_Tarefas = {}

class Tarefa(BaseModel):
    Tarefa: str
    Descricao: str
    Concluida: bool = False

@app.post("/adicionar")
def post_tarefas(tarefas:Tarefa):
    if tarefas.Tarefa in DB_Tarefas:
        raise HTTPException(status_code=404, detail="Essa tarefa já existe no banco de dados")
    else:
        DB_Tarefas[tarefas.Tarefa] = tarefas
        return {"message": "Tarefa adicionada"}

@app.get("/tarefas")
def get_tarefas():
    if not DB_Tarefas:
        raise HTTPException(status_code=400, detail="Banco de dados vazio")
    else:
        return DB_Tarefas
    
@app.put("/atualizar")
def put_tarefas(tarefas:Tarefa):
    if tarefas.Tarefa in DB_Tarefas:
        DB_Tarefas[tarefas.Tarefa].Concluida = tarefas.Concluida
        return {"message":"Tarefa atualizada com sucesso"}
    else:
        return {"message":"Tarefa não existe no banco de dados"}
    
@app.delete("/deletar/{nome_tarefa}")
def delete_tarefas(nome_tarefa: str):
    if nome_tarefa not in DB_Tarefas:
        raise {"message":"Essa tarefa não existe"}
    else:
        del DB_Tarefas[nome_tarefa]
        return {"message": "Tarefa removida com sucesso"}