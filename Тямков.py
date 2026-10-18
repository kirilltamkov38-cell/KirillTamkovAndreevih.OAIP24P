import json
import os

FILE_NAME = "projects.json"

def load_data():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_data(data):
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def show_projects():
    data = load_data()
    if not data:
        print("Список проектов пуст")
        return
    print("Список проектов:")
    for p in data:
        print(f"ID: {p['id']}, Название: {p['name']}, Статус: {p['status']}")

def create_project():
    name = input("Введите название проекта: ")
    data = load_data()
    new_id = len(data) + 1
    new_project = {
        "id": new_id,
        "name": name,
        "status": "Планирование",
        "tasks": []
    }
    data.append(new_project)
    save_data(data)
    print("Проект создан")

def add_task():
    try:
        p_id = int(input("Введите ID проекта: "))
        task_name = input("Введите название задачи: ")
        data = load_data()
        for p in data:
            if p["id"] == p_id:
                task = {
                    "name": task_name,
                    "status": "Новая"
                }
                p["tasks"].append(task)
                save_data(data)
                print("Задача добавлена")
                return
        print("Проект не найден")
    except ValueError:
        print("Ошибка ввода (ID должен быть числом)")

def show_tasks():
    try:
        p_id = int(input("Введите ID проекта: "))
        data = load_data()
        for p in data:
            if p["id"] == p_id:
                print(f"Задачи проекта '{p['name']}':")
                if not p["tasks"]:
                    print("Задач нет")
                else:
                    for t in p["tasks"]:
                        print(f"- {t['name']} ({t['status']})")
                return
        print("Проект не найден")
    except ValueError:
        print("Ошибка ввода (ID должен быть числом)")

def change_status():
    try:
        p_id = int(input("Введите ID проекта: "))
        print("1 - Планирование")
        print("2 - В работе")
        print("3 - Готов")
        choice = input("Выберите статус (цифру): ")
        
        statuses = {"1": "Планирование", "2": "В работе", "3": "Готов"}
        
        if choice in statuses:
            data = load_data()
            for p in data:
                if p["id"] == p_id:
                    p["status"] = statuses[choice]
                    save_data(data)
                    print("Статус изменен")
                    return
            print("Проект не найден")
        else:
            print("Неверный выбор статуса")
    except ValueError:
        print("Ошибка ввода (ID должен быть числом)")

while True:
    print("\n1 - Показать проекты")
    print("2 - Создать проект")
    print("3 - Добавить задачу")
    print("4 - Показать задачи")
    print("5 - Изменить статус")
    print("0 - Выход")
    
    choice = input("Выберите действие: ")
    
    if choice == "1":
        show_projects()
    elif choice == "2":
        create_project()
    elif choice == "3":
        add_task()
    elif choice == "4":
        show_tasks()
    elif choice == "5":
        change_status()
    elif choice == "0":
        break
    else:
        print("Неверный ввод")