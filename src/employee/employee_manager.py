import hashlib
from src.database.database import Database
from src.auth.auth import Auth


class EmployeeManager:
    def __init__(self, db_config):
        self.db = Database(db_config)
        self.auth = Auth(db_config)

    def create_employee(self, username, password, department_id):
        cursor = self.conn.cursor()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        cursor.execute(
            "INSERT INTO employees (username, password, department_id) VALUES (%s, %s, %s)",
            (username, hashed_password, department_id)
        )
        self.conn.commit()
        cursor.close()

    def delete_employee(self, employee_id):
        cursor = self.conn.cursor()
        cursor.execute(
            "DELETE FROM employees WHERE id = %s",
            (employee_id,)
        )
        self.conn.commit()
        cursor.close()

    def get_employees(self):
        query = "SELECT id, username, department_id FROM employees WHERE role = 'employee'"
        employees = self.db.fetchall(query)
        return employees
