import os

from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit,
    QListWidget, QComboBox, QTextEdit, QWidget, QMessageBox
)


class ManageTasks(QMainWindow):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.setWindowTitle("Управление задачами")
        self.setGeometry(150, 150, 600, 500)
        style_path = os.path.join(os.path.dirname(__file__), "../style.css")
        if os.path.exists(style_path):
            self.setStyleSheet(open(style_path).read())
        else:
            print("Файл style.css не найден!")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Список задач
        self.tasks_list = QListWidget()
        self.load_tasks()
        layout.addWidget(self.tasks_list)

        # Поля ввода
        self.task_title_input = QLineEdit()
        self.task_title_input.setPlaceholderText("Название задачи")
        layout.addWidget(self.task_title_input)

        self.task_description_input = QTextEdit()
        self.task_description_input.setPlaceholderText("Описание задачи")
        layout.addWidget(self.task_description_input)

        self.employee_select = QComboBox()
        self.load_employees()
        layout.addWidget(self.employee_select)

        # Кнопки управления
        button_layout = QHBoxLayout()

        self.add_btn = QPushButton("Добавить")
        self.add_btn.clicked.connect(self.add_task)
        button_layout.addWidget(self.add_btn)

        self.edit_btn = QPushButton("Обновить")
        self.edit_btn.clicked.connect(self.edit_task)
        button_layout.addWidget(self.edit_btn)

        self.delete_btn = QPushButton("Удалить")
        self.delete_btn.clicked.connect(self.delete_task)
        button_layout.addWidget(self.delete_btn)

        layout.addLayout(button_layout)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_tasks(self):
        """Загрузка списка задач из базы данных."""
        self.tasks_list.clear()
        tasks = self.db.fetchall(
            "SELECT tasks.id, tasks.title, users.username "
            "FROM tasks LEFT JOIN users ON tasks.employee_id = users.id"
        )
        for task in tasks:
            self.tasks_list.addItem(
                f"{task['id']}: {task['title']} (Назначена: {task['username'] or 'Не назначена'})"
            )

    def load_employees(self):
        """Загрузка списка сотрудников для выбора."""
        self.employee_select.clear()
        employees = self.db.fetchall(
            "SELECT id, username FROM users WHERE role = 'employee'"
        )
        self.employee_select.addItem("Не назначать", None)
        for employee in employees:
            self.employee_select.addItem(employee['username'], employee['id'])

    def add_task(self):
        title = self.task_title_input.text()
        description = self.task_description_input.toPlainText()
        employee_id = self.employee_select.currentData()  # Получаем ID сотрудника

        if not title or not employee_id:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля.")
            return

        try:
            self.db.execute(
                "INSERT INTO tasks (title, description, employee_id, status) VALUES (%s, %s, %s, %s)",
                (title, description, employee_id, "Не начато")
            )
            QMessageBox.information(self, "Успех", "Задача успешно создана.")
            self.load_tasks()
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось создать задачу: {e}")

    def edit_task(self):
        """Обновление выбранной задачи."""
        selected_item = self.tasks_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "Ошибка", "Выберите задачу для обновления.")
            return

        task_id = selected_item.text().split(":")[0]
        title = self.task_title_input.text().strip()
        description = self.task_description_input.toPlainText().strip()
        employee_id = self.employee_select.currentData()

        if not title or not description:
            QMessageBox.warning(self, "Ошибка", "Название и описание задачи не могут быть пустыми.")
            return

        try:
            self.db.execute(
                "UPDATE tasks SET title = %s, description = %s, employee_id = %s WHERE id = %s",
                (title, description, employee_id, task_id)
            )
            QMessageBox.information(self, "Успех", f"Задача обновлена на '{title}'.")
            self.load_tasks()
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось обновить задачу: {e}")

    def delete_task(self):
        """Удаление выбранной задачи."""
        selected_item = self.tasks_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "Ошибка", "Выберите задачу для удаления.")
            return

        task_id = selected_item.text().split(":")[0]

        try:
            self.db.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
            QMessageBox.information(self, "Успех", "Задача удалена.")
            self.load_tasks()
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось удалить задачу: {e}")
