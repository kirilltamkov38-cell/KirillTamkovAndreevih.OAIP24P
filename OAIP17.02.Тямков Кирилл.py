import json
import os

FILE = "projects.json"
STATUSES = ["Планирование", "В работе", "Готов"]

def load():
    if os.path.exists(FILE):
        with open(FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"projects": [], "next_id": 1}

def save(data):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def find(projects, pid):
    for p in projects:
        if p["id"] == pid:
            return p
    return None

def show_projects(projects):
    if not projects:
        print("\nНет проектов.")
        return
    print("\nПроекты:")
    for p in projects:
        print(f"{p['id']}: {p['name']} | {p['status']}")

def create(data):
    name = input("\nНазвание проекта: ").strip()
    if not name:
        print("Ошибка: пустое название.")
        return
    data["projects"].append({
        "id": data["next_id"],
        "name": name,
        "status": "Планирование",
        "tasks": []
    })
    data["next_id"] += 1
    save(data)
    print("Проект создан.")

def add_task(data):
    show_projects(data["projects"])
    if not data["projects"]:
        return
    try:
        pid = int(input("ID проекта: "))
    except:
        print("Ошибка ввода.")
        return
    proj = find(data["projects"], pid)
    if not proj:
        print("Проект не найден.")
        return
    desc = input("Описание задачи: ").strip()
    if not desc:
        print("Ошибка: пустое описание.")
        return
    proj["tasks"].append({"id": len(proj["tasks"])+1, "description": desc})
    save(data)
    print("Задача добавлена.")

def show_tasks(data):
    show_projects(data["projects"])
    if not data["projects"]:
        return
    try:
        pid = int(input("ID проекта: "))
    except:
        print("Ошибка ввода.")
        return
    proj = find(data["projects"], pid)
    if not proj:
        print("Проект не найден.")
        return
    if not proj["tasks"]:
        print("Нет задач.")
        return
    print(f"\nЗадачи проекта '{proj['name']}':")
    for t in proj["tasks"]:
        print(f"#{t['id']}: {t['description']}")

def change_status(data):
    show_projects(data["projects"])
    if not data["projects"]:
        return
    try:
        pid = int(input("ID проекта: "))
    except:
        print("Ошибка ввода.")
        return
    proj = find(data["projects"], pid)
    if not proj:
        print("Проект не найден.")
        return
    print(f"Текущий статус: {proj['status']}")
    for i, s in enumerate(STATUSES, 1):
        print(f"{i}. {s}")
    try:
        choice = int(input("Новый статус (номер): "))
        if 1 <= choice <= len(STATUSES):
            proj["status"] = STATUSES[choice-1]
            save(data)
            print("Статус обновлён.")
        else:
            print("Неверный номер.")
    except:
        print("Ошибка ввода.")

def main():
    data = load()
    while True:
        print("\nМЕНЮ:")
        print("1. Показать проекты")
        print("2. Создать проект")
        print("3. Добавить задачу")
        print("4. Показать задачи")
        print("5. Изменить статус")
        print("0. Выход")
        cmd = input("Выберите действие: ").strip()
        if cmd == "1":
            show_projects(data["projects"])
        elif cmd == "2":
            create(data)
        elif cmd == "3":
            add_task(data)
        elif cmd == "4":
            show_tasks(data)
        elif cmd == "5":
            change_status(data)
        elif cmd == "0":
            print("Выход.")
            break
        else:
            print("Неверная команда.")

if __name__ == "__main__":
    main()
