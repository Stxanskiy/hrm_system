from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QComboBox
from src.auth.auth import Auth


class AuthWindow(QDialog):
    def __init__(self, auth_manager, open_main_interface_callback):
        super().__init__()
        self.auth_manager = auth_manager
        self.open_main_interface_callback = open_main_interface_callback
        self.setWindowTitle("Авторизация")

        layout = QVBoxLayout()

        # Поля для ввода
        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Имя пользователя")
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Пароль")

        self.role_selector = QComboBox(self)
        self.role_selector.addItems(["admin", "employee"])

        # Кнопки
        self.login_button = QPushButton("Войти")
        self.login_button.clicked.connect(self.authenticate_user)

        layout.addWidget(QLabel("Вход в систему"))
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(QLabel("Выберите роль"))
        layout.addWidget(self.role_selector)
        layout.addWidget(self.login_button)
        self.setLayout(layout)

    def authenticate_user(self):
        username = self.username_input.text()
        password = self.password_input.text()
        role = self.role_selector.currentText()
        if self.auth_manager.login(username, password, role):
            self.open_main_interface_callback(role)
            self.accept()
        else:
            QMessageBox.warning(self, "Ошибка", "Неверное имя пользователя или пароль")
