from src.database.database import Database


class TaskManager:
    def __init__(self, db_config):
        self.db = Database(db_config)

    def create_task(self, name, employee_id):
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO tasks (name, employee_id, status) VALUES (%s, %s, 'start')",
            (name, employee_id)
        )
        self.conn.commit()
        cursor.close()

    def update_task_status(self, task_id, status):
        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE tasks SET status = %s WHERE id = %s",
            (status, task_id)
        )
        self.conn.commit()
        cursor.close()


    def delete_task(self, task_id):
        cursor = self.conn.cursor()
        cursor.execute(
            "DELETE FROM tasks WHERE id = %s",
            (task_id,)
        )
        self.conn.commit()
        cursor.close()

    def get_tasks_by_employee(self, employee_id):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT id, name, status FROM tasks WHERE employee_id = %s",
            (employee_id,)
        )
        tasks = cursor.fetchall()
        cursor.close()
        return tasks
