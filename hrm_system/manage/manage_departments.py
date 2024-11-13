import os

from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit,
    QListWidget, QWidget, QMessageBox
)


class ManageDepartments(QMainWindow):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.setWindowTitle("Управление отделами")
        self.setGeometry(150, 150, 500, 400)
        style_path = os.path.join(os.path.dirname(__file__), "../style.css")
        if os.path.exists(style_path):
            self.setStyleSheet(open(style_path).read())
        else:
            print("Файл style.css не найден!")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Список отделов
        self.departments_list = QListWidget()
        self.load_departments()
        layout.addWidget(self.departments_list)

        # Поле для ввода имени отдела
        self.department_input = QLineEdit()
        self.department_input.setPlaceholderText("Введите название отдела")
        layout.addWidget(self.department_input)

        # Кнопки управления
        button_layout = QHBoxLayout()

        self.add_btn = QPushButton("Добавить")
        self.add_btn.clicked.connect(self.add_department)
        button_layout.addWidget(self.add_btn)

        self.edit_btn = QPushButton("Обновить")
        self.edit_btn.clicked.connect(self.edit_department)
        button_layout.addWidget(self.edit_btn)

        self.delete_btn = QPushButton("Удалить")
        self.delete_btn.clicked.connect(self.delete_department)
        button_layout.addWidget(self.delete_btn)

        layout.addLayout(button_layout)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_departments(self):
        """Загрузка списка отделов из базы данных."""
        self.departments_list.clear()
        departments = self.db.fetchall("SELECT id, name FROM departments")
        for department in departments:
            self.departments_list.addItem(f"{department['id']}: {department['name']}")

    def add_department(self):
        """Добавление нового отдела."""
        department_name = self.department_input.text().strip()
        if not department_name:
            QMessageBox.warning(self, "Ошибка", "Название отдела не может быть пустым.")
            return

        try:
            self.db.execute("INSERT INTO departments (name) VALUES (%s)", (department_name,))
            QMessageBox.information(self, "Успех", f"Отдел '{department_name}' добавлен.")
            self.load_departments()
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось добавить отдел: {e}")

    def edit_department(self):
        """Обновление выбранного отдела."""
        selected_item = self.departments_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "Ошибка", "Выберите отдел для обновления.")
            return

        department_id = selected_item.text().split(":")[0]
        department_name = self.department_input.text().strip()
        if not department_name:
            QMessageBox.warning(self, "Ошибка", "Название отдела не может быть пустым.")
            return

        try:
            self.db.execute(
                "UPDATE departments SET name = %s WHERE id = %s",
                (department_name, department_id)
            )
            QMessageBox.information(self, "Успех", f"Отдел обновлен на '{department_name}'.")
            self.load_departments()
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось обновить отдел: {e}")

    def delete_department(self):
        """Удаление выбранного отдела."""
        selected_item = self.departments_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "Ошибка", "Выберите отдел для удаления.")
            return

        department_id = selected_item.text().split(":")[0]

        try:
            self.db.execute("DELETE FROM departments WHERE id = %s", (department_id,))
            QMessageBox.information(self, "Успех", "Отдел удален.")
            self.load_departments()
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось удалить отдел: {e}")
