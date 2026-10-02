import sqlite3

DB_NAME = "students.db"


def create_table(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            group_name TEXT NOT NULL,
            grade INTEGER NOT NULL,
            age INTEGER
        )
    """)

    # Если база уже была создана без поля age — добавляем его
    cursor.execute("PRAGMA table_info(students)")
    columns = [row[1] for row in cursor.fetchall()]
    if "age" not in columns:
        cursor.execute("ALTER TABLE students ADD COLUMN age INTEGER")

    conn.commit()


def seed_data(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM students")
    count = cursor.fetchone()[0]

    if count == 0:
        students = [
            ("Иванов Иван", "ИСП-101", 5, 18),
            ("Петров Пётр", "ИСП-101", 4, 18),
            ("Сидоров Алексей", "ИСП-102", 3, 19),
            ("Смирнова Анна", "ИСП-102", 5, 18),
            ("Кузнецов Максим", "ИСП-101", 4, 19),
        ]
        cursor.executemany(
            "INSERT INTO students (name, group_name, grade, age) VALUES (?, ?, ?, ?)",
            students
        )
        conn.commit()


def print_students(rows):
    if not rows:
        print("Записи не найдены.")
        return

    print("-" * 72)
    print(f"{'ID':<4} {'ФИО':<25} {'Группа':<12} {'Оценка':<7} {'Возраст':<8}")
    print("-" * 72)

    for row in rows:
        student_id, name, group_name, grade, age = row
        age_text = str(age) if age is not None else "-"
        print(f"{student_id:<4} {name:<25} {group_name:<12} {grade:<7} {age_text:<8}")

    print("-" * 72)


def input_int(prompt, min_value=None, max_value=None, allow_empty=False):
    while True:
        raw = input(prompt).strip()

        if allow_empty and raw == "":
            return None

        try:
            value = int(raw)
        except ValueError:
            print("Ошибка: нужно ввести целое число.")
            continue

        if min_value is not None and value < min_value:
            print(f"Ошибка: число должно быть не меньше {min_value}.")
            continue

        if max_value is not None and value > max_value:
            print(f"Ошибка: число должно быть не больше {max_value}.")
            continue

        return value


def input_grade():
    return input_int("Введите оценку (2-5): ", 2, 5)


def show_all(conn):
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, name, group_name, grade, age FROM students ORDER BY id"
    )
    print_students(cursor.fetchall())


def add_student(conn):
    name = input("Введите ФИО: ").strip()
    if not name:
        print("ФИО не может быть пустым.")
        return

    group_name = input("Введите группу: ").strip()
    if not group_name:
        print("Название группы не может быть пустым.")
        return

    grade = input_grade()
    age = input_int(
        "Введите возраст (Enter — не указывать): ",
        1,
        120,
        allow_empty=True
    )

    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO students (name, group_name, grade, age) VALUES (?, ?, ?, ?)",
        (name, group_name, grade, age)
    )
    conn.commit()
    print("Студент добавлен.")


def find_by_group(conn):
    group_name = input("Введите название группы: ").strip()

    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, name, group_name, grade, age "
        "FROM students WHERE group_name = ? ORDER BY name",
        (group_name,)
    )
    print_students(cursor.fetchall())


def find_by_grade(conn):
    grade = input_grade()

    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, name, group_name, grade, age "
        "FROM students WHERE grade = ? ORDER BY name",
        (grade,)
    )
    print_students(cursor.fetchall())


def update_grade(conn):
    show_all(conn)
    student_id = input_int("Введите ID студента: ", 1)

    cursor = conn.cursor()
    cursor.execute("SELECT id FROM students WHERE id = ?", (student_id,))
    if cursor.fetchone() is None:
        print("Студент с таким ID не найден.")
        return

    new_grade = input_grade()
    cursor.execute(
        "UPDATE students SET grade = ? WHERE id = ?",
        (new_grade, student_id)
    )
    conn.commit()
    print("Оценка изменена.")
    show_all(conn)


def delete_student(conn):
    show_all(conn)
    student_id = input_int("Введите ID студента для удаления: ", 1)

    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()

    if cursor.rowcount == 0:
        print("Студент с таким ID не найден.")
    else:
        print("Студент удалён.")

    show_all(conn)


# Дополнительные задания
def students_older_than(conn):
    age = input_int("Введите возраст: ", 1, 120)

    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, name, group_name, grade, age "
        "FROM students WHERE age > ? ORDER BY age",
        (age,)
    )
    print_students(cursor.fetchall())


def average_grade(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT AVG(grade) FROM students")
    avg = cursor.fetchone()[0]

    if avg is None:
        print("Нет данных для расчёта.")
    else:
        print(f"Средняя оценка всех студентов: {avg:.2f}")


def count_by_group(conn):
    cursor = conn.cursor()
    cursor.execute(
        "SELECT group_name, COUNT(*) "
        "FROM students GROUP BY group_name ORDER BY group_name"
    )
    rows = cursor.fetchall()

    if not rows:
        print("Нет данных.")
        return

    print("Количество студентов в каждой группе:")
    for group_name, count in rows:
        print(f"{group_name}: {count}")


def best_student(conn):
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, name, group_name, grade, age "
        "FROM students ORDER BY grade DESC, name ASC LIMIT 1"
    )
    row = cursor.fetchone()

    if row is None:
        print("Нет данных.")
    else:
        print("Студент с самой высокой оценкой:")
        print_students([row])


def print_menu():
    print("\n====== УЧЁТ СТУДЕНТОВ ======")
    print("1. Показать всех студентов")
    print("2. Добавить студента")
    print("3. Найти студентов по группе")
    print("4. Найти студентов по оценке")
    print("5. Изменить оценку")
    print("6. Удалить студента")
    print("7. Доп.: студенты старше указанного возраста")
    print("8. Доп.: средняя оценка")
    print("9. Доп.: количество студентов по группам")
    print("10. Доп.: студент с самой высокой оценкой")
    print("0. Выход")


def main():
    conn = sqlite3.connect(DB_NAME)

    try:
        create_table(conn)
        seed_data(conn)

        while True:
            print_menu()
            choice = input("Выберите пункт: ").strip()

            if choice == "1":
                show_all(conn)
            elif choice == "2":
                add_student(conn)
            elif choice == "3":
                find_by_group(conn)
            elif choice == "4":
                find_by_grade(conn)
            elif choice == "5":
                update_grade(conn)
            elif choice == "6":
                delete_student(conn)
            elif choice == "7":
                students_older_than(conn)
            elif choice == "8":
                average_grade(conn)
            elif choice == "9":
                count_by_group(conn)
            elif choice == "10":
                best_student(conn)
            elif choice == "0":
                print("Выход из программы.")
                break
            else:
                print("Нет такого пункта меню. Попробуйте снова.")

    except KeyboardInterrupt:
        print("\nПрограмма прервана пользователем.")
    finally:
        conn.close()


if __name__ == "__main__":
    main()