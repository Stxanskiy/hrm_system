from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QLabel, QListWidget, QComboBox, QPushButton, QHBoxLayout, QWidget, QMessageBox
)
from hashlib import sha256
from db.database import Database

class EmployeePanel(QMainWindow):
    def __init__(self, db, user):
        super().__init__()
        self.db = db
        self.user = user  # Сохраняем объект пользователя
        self.setWindowTitle(f"Добро пожаловать, {self.user['username']}")  # Заголовок окна
        self.setGeometry(150, 150, 600, 500)
        self.setStyleSheet(open("style.css").read())
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Приветствие
        welcome_label = QLabel(f"Ваши задачи, {self.user['username']}:")
        layout.addWidget(welcome_label)

        # Список задач
        self.task_list = QListWidget()  # Объявляем task_list
        self.load_tasks()  # Загружаем задачи
        layout.addWidget(self.task_list)

        # Выбор статуса
        self.status_select = QComboBox()
        self.status_select.addItems(["Не начато", "В процессе", "Завершено"])
        layout.addWidget(self.status_select)

        # Кнопки управления
        button_layout = QHBoxLayout()

        self.update_status_btn = QPushButton("Обновить статус")
        self.update_status_btn.clicked.connect(self.update_task_status)
        button_layout.addWidget(self.update_status_btn)

        layout.addLayout(button_layout)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_tasks(self):
        """Загрузка задач сотрудника."""
        self.task_list.clear()  # Используем self.task_list
        try:
            tasks = self.db.fetchall(
                "SELECT * FROM tasks WHERE employee_id = %s", (self.user['id'],)
            )
            for task in tasks:
                self.task_list.addItem(f"{task['title']} - {task['status']}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить задачи: {str(e)}")

    def update_task_status(self):
        """Обновление статуса задачи."""
        selected_task = self.task_list.currentItem()
        if not selected_task:
            QMessageBox.warning(self, "Ошибка", "Выберите задачу для обновления.")
            return

        new_status = self.status_select.currentText()
        task_title = selected_task.text().split(" - ")[0]

        try:
            self.db.execute(
                "UPDATE tasks SET status = %s WHERE title = %s AND employee_id = %s",
                (new_status, task_title, self.user['id'])
            )
            QMessageBox.information(self, "Успех", "Статус задачи обновлен.")
            self.load_tasks()  # Обновляем список задач
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось обновить статус: {str(e)}")
