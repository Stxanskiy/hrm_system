import os

from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QPushButton, QWidget, QMessageBox
)
from hrm_system.manage.manage_departments import ManageDepartments
from hrm_system.manage.manage_employees import ManageEmployees
from hrm_system.manage.manage_tasks import ManageTasks

class AdminPanel(QMainWindow):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.setWindowTitle("HRM System - Панель администратора")
        self.setGeometry(100, 100, 600, 400)
        style_path = os.path.join(os.path.dirname(__file__), "../style.css")
        if os.path.exists(style_path):
            self.setStyleSheet(open(style_path).read())
        else:
            print("Файл style.css не найден!")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.add_employee_btn = QPushButton("Добавить сотрудника")
        self.add_employee_btn.clicked.connect(self.add_employee)
        layout.addWidget(self.add_employee_btn)

        self.manage_departments_btn = QPushButton("Управление отделами")
        self.manage_departments_btn.clicked.connect(self.manage_departments)
        layout.addWidget(self.manage_departments_btn)

        self.manage_tasks_btn = QPushButton("Управление задачами")
        self.manage_tasks_btn.clicked.connect(self.manage_tasks)  # Открываем окно управления задачами
        layout.addWidget(self.manage_tasks_btn)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def add_employee(self):
        """Открывает окно управления сотрудниками."""
        self.employees_window = ManageEmployees(self.db)
        self.employees_window.show()
    def manage_departments(self):
        """Управление отделами."""
        QMessageBox.information(self, "Функция", "Здесь будет управление отделами.")

    def create_task(self):
        """Создание задачи."""
        QMessageBox.information(self, "Функция", "Здесь будет создание задач.")

    def manage_departments(self):
        """Открывает окно управления отделами."""
        self.departments_window = ManageDepartments(self.db)
        self.departments_window.show()


    def manage_tasks(self):
        """Открывает окно управления задачами."""
        self.tasks_window = ManageTasks(self.db)
        self.tasks_window.show()