import os
from hashlib import sha256

from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit,
    QListWidget, QComboBox, QWidget, QMessageBox
)


class ManageEmployees(QMainWindow):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.setWindowTitle("Управление сотрудниками")
        self.setGeometry(150, 150, 600, 500)

        # Получаем абсолютный путь к файлу style.css
        style_path = os.path.join(os.path.dirname(__file__), "../style.css")
        if os.path.exists(style_path):
            self.setStyleSheet(open(style_path).read())
        else:
            print("Файл style.css не найден!")

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Список сотрудников
        self.employees_list = QListWidget()
        self.load_employees()
        layout.addWidget(self.employees_list)

        # Поля ввода
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Логин сотрудника")
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Пароль сотрудника")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)

        self.department_select = QComboBox()
        self.load_departments()
        layout.addWidget(self.department_select)

        # Кнопки управления
        button_layout = QHBoxLayout()

        self.add_btn = QPushButton("Добавить")
        self.add_btn.clicked.connect(self.add_employee)
        button_layout.addWidget(self.add_btn)

        self.delete_btn = QPushButton("Удалить")
        self.delete_btn.clicked.connect(self.delete_employee)
        button_layout.addWidget(self.delete_btn)

        layout.addLayout(button_layout)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_employees(self):
        """Загрузка списка сотрудников из базы данных."""
        self.employees_list.clear()
        employees = self.db.fetchall(
            "SELECT users.id, users.username, departments.name AS department "
            "FROM users LEFT JOIN departments ON users.department_id = departments.id "
            "WHERE users.role = 'employee'"
        )
        for employee in employees:
            self.employees_list.addItem(
                f"{employee['id']}: {employee['username']} ({employee['department'] or 'Без отдела'})"
            )

    def load_departments(self):
        """Загрузка списка отделов для выбора."""
        self.department_select.clear()
        departments = self.db.fetchall("SELECT id, name FROM departments")
        self.department_select.addItem("Без отдела", None)
        for department in departments:
            self.department_select.addItem(department['name'], department['id'])

    def add_employee(self):
        """Добавление нового сотрудника."""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        department_id = self.department_select.currentData()

        if not username or not password:
            QMessageBox.warning(self, "Ошибка", "Логин и пароль не могут быть пустыми.")
            return

        password_hash = sha256(password.encode()).hexdigest()
        try:
            self.db.execute(
                "INSERT INTO users (username, password_hash, role, department_id) VALUES (%s, %s, 'employee', %s)",
                (username, password_hash, department_id)
            )
            QMessageBox.information(self, "Успех", f"Сотрудник '{username}' добавлен.")
            self.load_employees()
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось добавить сотрудника: {e}")

    def delete_employee(self):
        """Удаление выбранного сотрудника."""
        selected_item = self.employees_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "Ошибка", "Выберите сотрудника для удаления.")
            return

        employee_id = selected_item.text().split(":")[0]

        try:
            self.db.execute("DELETE FROM users WHERE id = %s", (employee_id,))
            QMessageBox.information(self, "Успех", "Сотрудник удален.")
            self.load_employees()
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось удалить сотрудника: {e}")
