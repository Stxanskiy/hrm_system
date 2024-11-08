from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLineEdit, QLabel, QListWidget
from src.auth.auth import Auth
from src.departament.departament_manager import DepartmentManager
from src.employee.employee_manager import EmployeeManager
from src.task.task_manager import TaskManager

class MainWindow(QMainWindow):
    def __init__(self, db_config):
        super().__init__()
        self.setWindowTitle("HR System - Admin")
        self.setGeometry(300, 300, 500, 400)

        # Initialize managers
        self.auth = Auth(db_config)
        self.department_manager = DepartmentManager(db_config)
        self.employee_manager = EmployeeManager(db_config)
        self.task_manager = TaskManager(db_config)

        # UI setup
        self.layout = QVBoxLayout()

        # Add widgets for department management
        self.init_department_management_ui()

        # Add widgets for employee management
        self.init_employee_management_ui()

        # Add widgets for task management
        self.init_task_management_ui()

        # Container
        self.container = QWidget()
        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)

    def init_department_management_ui(self):
        self.layout.addWidget(QLabel("Управление отделами"))

        # Department creation
        self.department_input = QLineEdit(self)
        self.department_input.setPlaceholderText("Название отдела")
        self.create_department_button = QPushButton("Создать отдел", self)
        self.create_department_button.clicked.connect(self.create_department)
        self.layout.addWidget(self.department_input)
        self.layout.addWidget(self.create_department_button)

        # Department deletion
        self.delete_department_id_input = QLineEdit(self)
        self.delete_department_id_input.setPlaceholderText("ID отдела для удаления")
        self.delete_department_button = QPushButton("Удалить отдел", self)
        self.delete_department_button.clicked.connect(self.delete_department)
        self.layout.addWidget(self.delete_department_id_input)
        self.layout.addWidget(self.delete_department_button)

        # Department list
        self.department_list = QListWidget(self)
        self.load_departments()
        self.layout.addWidget(self.department_list)

    def init_employee_management_ui(self):
        self.layout.addWidget(QLabel("Управление сотрудниками"))

        # Employee creation
        self.username_input = QLineEdit(self)
        self.password_input = QLineEdit(self)
        self.department_id_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Логин сотрудника")
        self.password_input.setPlaceholderText("Пароль")
        self.department_id_input.setPlaceholderText("ID отдела")

        self.create_employee_button = QPushButton("Добавить сотрудника", self)
        self.create_employee_button.clicked.connect(self.create_employee)

        self.layout.addWidget(self.username_input)
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(self.department_id_input)
        self.layout.addWidget(self.create_employee_button)

        # Employee deletion
        self.delete_employee_id_input = QLineEdit(self)
        self.delete_employee_id_input.setPlaceholderText("ID сотрудника для удаления")
        self.delete_employee_button = QPushButton("Удалить сотрудника", self)
        self.delete_employee_button.clicked.connect(self.delete_employee)
        self.layout.addWidget(self.delete_employee_id_input)
        self.layout.addWidget(self.delete_employee_button)

    def init_task_management_ui(self):
        self.layout.addWidget(QLabel("Управление задачами"))

        # Task creation
        self.task_name_input = QLineEdit(self)
        self.employee_id_input = QLineEdit(self)
        self.task_name_input.setPlaceholderText("Название задачи")
        self.employee_id_input.setPlaceholderText("ID сотрудника")

        self.create_task_button = QPushButton("Назначить задачу", self)
        self.create_task_button.clicked.connect(self.create_task)

        self.layout.addWidget(self.task_name_input)
        self.layout.addWidget(self.employee_id_input)
        self.layout.addWidget(self.create_task_button)

        # Task deletion
        self.delete_task_id_input = QLineEdit(self)
        self.delete_task_id_input.setPlaceholderText("ID задачи для удаления")
        self.delete_task_button = QPushButton("Удалить задачу", self)
        self.delete_task_button.clicked.connect(self.delete_task)
        self.layout.addWidget(self.delete_task_id_input)
        self.layout.addWidget(self.delete_task_button)


    def create_department(self):
        department_name = self.department_input.text()
        self.department_manager.create_department(department_name)
        self.load_departments()

    def load_departments(self):
        self.department_list.clear()
        departments = self.department_manager.get_departments()
        for dept in departments:
            self.department_list.addItem(f"ID: {dept[0]}, Name: {dept[1]}")


    def delete_department(self):
        department_id = int(self.delete_department_input.text())
        self.department_manager.delete_department(department_id)
        self.load_departments()  # Refresh department list

    def create_employee(self):
        username = self.username_input.text()
        password = self.password_input.text()
        department_id = int(self.department_id_input.text())
        self.employee_manager.create_employee(username, password, department_id)
        print(f"Employee '{username}' added successfully.")

    def delete_employee(self):
        employee_id = int(self.delete_employee_id_input.text())
        self.employee_manager.delete_employee(employee_id)
        print(f"Employee with ID {employee_id} deleted successfully.")

    def create_task(self):
        task_name = self.task_name_input.text()
        employee_id = int(self.employee_id_input.text())
        self.task_manager.create_task(task_name, employee_id)
        print(f"Task '{task_name}' assigned to employee with ID {employee_id}.")

    def delete_task(self):
        task_id = int(self.delete_task_input.text())
        self.task_manager.delete_task(task_id)
        print(f"Task with ID {task_id} deleted successfully.")


    def view_tasks(self):
        employee_id = int(self.employee_id_input.text())
        tasks = self.task_manager.get_tasks_by_employee(employee_id)
        self.task_list.clear()
        for task in tasks:
            self.task_list.addItem(f"ID: {task[0]}, Name: {task[1]}, Status: {task[2]}")

    def update_task_status(self):
        selected_task = self.task_list.currentItem()
        if selected_task:
            task_id = int(selected_task.text().split(",")[0].split(":")[1].strip())
            new_status = self.status_combo.currentText()
            self.task_manager.update_task_status(task_id, new_status)
            self.view_tasks()  # Refresh task list  # Refresh tasks list  # обновление списка задач после изменения статуса