import psycopg2

class DepartmentManager:
    def __init__(self, db_config):
        self.conn = psycopg2.connect(**db_config)

    def create_department(self, name):
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO departments (name) VALUES (%s)",
            (name,)
        )
        self.conn.commit()
        cursor.close()

    def delete_department(self, department_id):
        cursor = self.conn.cursor()
        cursor.execute(
            "DELETE FROM departments WHERE id = %s",
            (department_id,)
        )
        self.conn.commit()
        cursor.close()

    def get_departments(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM departments")
        departments = cursor.fetchall()
        cursor.close()
        return departments
