import sys
from PyQt6.QtWidgets import QApplication
from src.auth.auth import Auth
from src.auth.auth_window import AuthWindow
from ui import MainWindow

def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(open("style.css").read())

    db_config = {
        "dbname": "hrm_system",
        "user": "postgres",
        "password": "456456",
        "host": "localhost",
        "port": "5432"
    }
    auth = Auth(db_config)

    def open_main_interface(role):
        window = MainWindow(role, db_config)
        window.show()

    auth_window = AuthWindow(auth, open_main_interface)
    auth_window.exec()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
