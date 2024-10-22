import os
import requests
import json

# Константы для API
API_BASE_URL = "http://127.0.0.1:8000/notes"
TOKEN_FILE = "token.txt"


# Функция для получения токена из файла
def get_token():
    if not os.path.exists(TOKEN_FILE):
        print("Токен не найден. Убедитесь, что он сохранён в token.txt.")
        return None
    with open(TOKEN_FILE, 'r') as f:
        return f.read().strip()


# Функция для создания заметки
def create_note():
    token = get_token()
    if not token:
        return

    text = input("Введите текст заметки: ")
    response = requests.post(
        f"{API_BASE_URL}/",
        params={"token": token},
        data={"text": text}
    )

    if response.status_code == 200:
        print(f"Заметка создана с ID: {response.json()['id']}")
    else:
        print(f"Ошибка создания заметки: {response.text}")


# Функция для чтения заметки по ID
def read_note():
    token = get_token()
    if not token:
        return

    note_id = input("Введите ID заметки: ")
    response = requests.get(
        f"{API_BASE_URL}/{note_id}",
        params={"token": token}
    )

    if response.status_code == 200:
        note = response.json()
        print(f"ID: {note['id']}\nТекст: {note['text']}")
    else:
        print(f"Ошибка получения заметки: {response.text}")


# Функция для получения информации о заметке
def get_note_info():
    token = get_token()
    if not token:
        return

    note_id = input("Введите ID заметки: ")
    response = requests.get(
        f"{API_BASE_URL}/{note_id}/info",
        params={"token": token}
    )

    if response.status_code == 200:
        info = response.json()
        print(f"Создано: {info['created_at']}\nОбновлено: {info['updated_at']}")
    else:
        print(f"Ошибка получения информации о заметке: {response.text}")


# Функция для обновления текста заметки
def update_note():
    token = get_token()
    if not token:
        return

    note_id = input("Введите ID заметки: ")
    new_text = input("Введите новый текст заметки: ")
    response = requests.patch(
        f"{API_BASE_URL}/{note_id}",
        params={"token": token},
        data={"text": new_text}
    )

    if response.status_code == 200:
        print("Заметка обновлена.")
    else:
        print(f"Ошибка обновления заметки: {response.text}")


# Функция для удаления заметки
def delete_note():
    token = get_token()
    if not token:
        return

    note_id = input("Введите ID заметки: ")
    response = requests.delete(
        f"{API_BASE_URL}/{note_id}",
        params={"token": token}
    )

    if response.status_code == 200:
        print("Заметка удалена.")
    else:
        print(f"Ошибка удаления заметки: {response.text}")


# Функция для получения списка заметок
def list_notes():
    token = get_token()
    if not token:
        return

    response = requests.get(
        f"{API_BASE_URL}/",
        params={"token": token}
    )

    if response.status_code == 200:
        notes = response.json()
        print("Список заметок:")
        for i, note_id in notes.items():
            print(f"{i}: {note_id}")
    else:
        print(f"Ошибка получения списка заметок: {response.text}")


# Меню для работы с клиентом
def main():
    while True:
        print("\nВыберите действие:")
        print("1. Создать заметку")
        print("2. Прочитать заметку по ID")
        print("3. Получить информацию о заметке")
        print("4. Обновить заметку")
        print("5. Удалить заметку")
        print("6. Получить список заметок")
        print("0. Выйти")

        choice = input("\nВаш выбор: ")

        if choice == "1":
            create_note()
        elif choice == "2":
            read_note()
        elif choice == "3":
            get_note_info()
        elif choice == "4":
            update_note()
        elif choice == "5":
            delete_note()
        elif choice == "6":
            list_notes()
        elif choice == "0":
            print("До свидания!")
            break
        else:
            print("Некорректный выбор. Пожалуйста, попробуйте снова.")


if __name__ == "__main__":
    main()
