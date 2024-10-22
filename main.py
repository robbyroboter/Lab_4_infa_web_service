from fastapi import FastAPI, HTTPException, Depends, Body
from pydantic import BaseModel
from typing import List, Dict
from datetime import datetime
import os
import json

app = FastAPI()

# Директория для хранения заметок
NOTES_DIR = "notes"
TOKENS_FILE = "tokens.txt"

# Убедимся, что директория существует
os.makedirs(NOTES_DIR, exist_ok=True)


# Модели для создания заметок
class Note(BaseModel):
    id: int
    text: str


class NoteInfo(BaseModel):
    created_at: str
    updated_at: str


# Авторизация с помощью токенов
def verify_token(token: str):
    if not os.path.exists(TOKENS_FILE):
        raise HTTPException(status_code=403, detail="Access Denied")

    with open(TOKENS_FILE, 'r') as f:
        tokens = f.read().splitlines()

    if token not in tokens:
        raise HTTPException(status_code=403, detail="Access Denied")


# Метод для чтения данных заметки
def read_note_file(note_id: int):
    note_file = os.path.join(NOTES_DIR, f"{note_id}.json")
    if not os.path.exists(note_file):
        raise HTTPException(status_code=404, detail="Note not found")

    with open(note_file, 'r') as f:
        return json.load(f)


# 1. Создать заметку (POST)
@app.post("/notes/", response_model=Note)
def create_note(text: str = Body(...), token: str = Depends(verify_token)):
    note_id = len(os.listdir(NOTES_DIR)) + 1
    created_at = updated_at = datetime.now().isoformat()

    note_data = {
        "id": note_id,
        "text": text,
        "created_at": created_at,
        "updated_at": updated_at
    }

    note_file = os.path.join(NOTES_DIR, f"{note_id}.json")
    with open(note_file, 'w') as f:
        json.dump(note_data, f)

    return note_data


# 2. Прочитать заметку по ID (GET)
@app.get("/notes/{note_id}", response_model=Note)
def get_note(note_id: int, token: str = Depends(verify_token)):
    note_data = read_note_file(note_id)
    return {"id": note_data["id"], "text": note_data["text"]}


# 3. Получить информацию о времени создания и изменения заметки (GET)
@app.get("/notes/{note_id}/info", response_model=NoteInfo)
def get_note_info(note_id: int, token: str = Depends(verify_token)):
    note_data = read_note_file(note_id)
    return {
        "created_at": note_data["created_at"],
        "updated_at": note_data["updated_at"]
    }


# 4. Обновить текст заметки (PATCH)
@app.patch("/notes/{note_id}")
def update_note(note_id: int, text: str = Body(...), token: str = Depends(verify_token)):
    note_data = read_note_file(note_id)
    note_data["text"] = text
    note_data["updated_at"] = datetime.now().isoformat()

    note_file = os.path.join(NOTES_DIR, f"{note_id}.json")
    with open(note_file, 'w') as f:
        json.dump(note_data, f)

    return {"status": "updated"}


# 5. Удалить заметку (DELETE)
@app.delete("/notes/{note_id}")
def delete_note(note_id: int, token: str = Depends(verify_token)):
    note_file = os.path.join(NOTES_DIR, f"{note_id}.json")
    if os.path.exists(note_file):
        os.remove(note_file)
        return {"status": "deleted"}
    raise HTTPException(status_code=404, detail="Note not found")


# 6. Получить список ID всех заметок (GET)
@app.get("/notes/", response_model=Dict[int, int])
def list_notes(token: str = Depends(verify_token)):
    note_ids = {i: int(note.replace(".json", "")) for i, note in enumerate(os.listdir(NOTES_DIR))}
    return note_ids

