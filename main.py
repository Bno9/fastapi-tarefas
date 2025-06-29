from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Optional
import secrets
import os


usuario = 'ADMIN'
senha = '123'

security = HTTPBasic()

app = FastAPI()

DB_Tarefas = {}

class Tarefa(BaseModel):
    Tarefa: str
    Descricao: str
    Concluida: bool = False

def autenticar_usuario(credentials: HTTPBasicCredentials = Depends(security)):
    is_username_correct = secrets.compare_digest(credentials.username, usuario)
    is_password_correct = secrets.compare_digest(credentials.password, senha)

    if not (is_password_correct and is_username_correct):
        raise HTTPException(
            status_code=401,
            detail="Usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Basic"}
        )

@app.post("/adicionar")
def post_tarefas(tarefas:Tarefa, credentials: HTTPBasicCredentials = Depends(autenticar_usuario)):
    if tarefas.Tarefa in DB_Tarefas:
        raise HTTPException(status_code=404, detail="Essa tarefa já existe no banco de dados")
    else:
        DB_Tarefas[tarefas.Tarefa] = tarefas
        return {"message": "Tarefa adicionada"}

@app.get("/tarefas")
def get_tarefas(page: int = 1, limit: int = 10, credentials: HTTPBasicCredentials = Depends(autenticar_usuario)):
    if not DB_Tarefas:
        raise HTTPException(status_code=400, detail="Banco de dados vazio")
    else:
        return DB_Tarefas
    
@app.put("/atualizar")
def put_tarefas(tarefas:Tarefa, credentials: HTTPBasicCredentials = Depends(autenticar_usuario)):
    if tarefas.Tarefa in DB_Tarefas and tarefas.Concluida != DB_Tarefas[tarefas.Tarefa].Concluida:
        DB_Tarefas[tarefas.Tarefa].Concluida = tarefas.Concluida
        return {"message":"Tarefa atualizada com sucesso"}
    else:
        raise HTTPException(status_code=400, detail="Tarefa não existe ou já está com esse status.")
    
@app.delete("/deletar/{nome_tarefa}")
def delete_tarefas(nome_tarefa: str, credentials: HTTPBasicCredentials = Depends(autenticar_usuario)):
    if nome_tarefa not in DB_Tarefas:
        raise HTTPException(status_code=400, detail="Essa tarefa não existe")
    else:
        del DB_Tarefas[nome_tarefa]
        return {"message": "Tarefa removida com sucesso"}