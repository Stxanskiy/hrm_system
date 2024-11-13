import os

from PyQt6.QtWidgets import (
    QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox
)
from hashlib import sha256


class Auth(QMainWindow):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.setWindowTitle("HRM System - Авторизация")
        self.setGeometry(100, 100, 400, 300)
        style_path = os.path.join(os.path.dirname(__file__), "../style.css")
        if os.path.exists(style_path):
            self.setStyleSheet(open(style_path).read())
        else:
            print("Файл style.css не найден!")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.label = QLabel("Введите логин и пароль:")
        layout.addWidget(self.label)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Логин")
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)

        self.login_button = QPushButton("Войти")
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)

        self.register_button = QPushButton("Регистрация")
        self.register_button.clicked.connect(self.register)
        layout.addWidget(self.register_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def login(self):
        """Метод для входа в систему."""
        username = self.username_input.text()
        password = sha256(self.password_input.text().encode()).hexdigest()

        user = self.db.fetchone(
            "SELECT * FROM users WHERE username = %s AND password_hash = %s",
            (username, password)
        )

        if user:
            if user['role'] == 'admin':
                from hrm_system.admin_panel import AdminPanel
                self.admin_panel = AdminPanel(self.db)
                self.admin_panel.show()
                self.close()
            else:
                from hrm_system.employee_panel import EmployeePanel
                self.employee_panel = EmployeePanel(self.db, user)  # Передаем весь объект user
                self.employee_panel.show()
                self.close()
        else:
            QMessageBox.warning(self, "Ошибка", "Неверные логин или пароль.")
    def register(self):
        """Метод для регистрации администратора."""
        username = self.username_input.text()
        password = sha256(self.password_input.text().encode()).hexdigest()

        try:
            self.db.execute(
                "INSERT INTO users (username, password_hash, role) VALUES (%s, %s, 'admin')",
                (username, password)
            )
            QMessageBox.information(self, "Успех", "Администратор зарегистрирован.")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Ошибка регистрации: {e}")

    def open_employee_panel(self, user):
        """Открытие интерфейса сотрудника."""
        from employee_panel import EmployeePanel

        self.employee_window = EmployeePanel(self.db, user)
        self.employee_window.show()
        self.close()