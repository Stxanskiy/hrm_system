import os

def load_stylesheet():
    """Загружает файл style.css."""
    style_path = os.path.join(os.path.dirname(__file__), "style.css")
    if os.path.exists(style_path):
        with open(style_path, "r") as file:
            return file.read()
    else:
        print("Файл style.css не найден!")
        return ""
