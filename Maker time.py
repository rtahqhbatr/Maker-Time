import sys  # імпортуємо модуль sys для роботи з аргументами командного рядка і виходом з програми
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton
# імпортуємо основні віджети PyQt5:
# QApplication — керує основним циклом подій,
# QWidget — базовий клас для вікон,
# QLabel — віджет для тексту,
# QVBoxLayout — вертикальний layout для розташування віджетів,
# QPushButton — кнопка

from PyQt5.QtGui import QPixmap, QIcon  # імпортуємо QPixmap для роботи з зображеннями, QIcon — для іконок кнопок
from PyQt5.QtCore import QSize  # імпортуємо QSize для задання розмірів елементів

class WatermelonClicker(QWidget):  # створюємо клас нашого головного вікна, наслідуючи QWidget
    def __init__(self):
        super().__init__()  # ініціалізуємо базовий клас QWidget
        self.setWindowTitle("Арбуз Клікер")  # встановлюємо заголовок вікна
        self.click_count = 0  # змінна для зберігання кількості кліків

        # Створюємо вертикальний layout, щоб розташувати віджети один під одним
        layout = QVBoxLayout()

        # Створюємо QLabel для відображення рахунку кліків
        self.label = QLabel("Кількість кліків: 0")  # початковий текст
        self.label.setStyleSheet("font-size: 20px;")  # встановлюємо розмір шрифту через CSS-стилі
        layout.addWidget(self.label)  # додаємо label до layout'у

        # Створюємо кнопку, на яку будемо додавати зображення арбуза
        self.button = QPushButton()
        self.button.setIcon(QIcon("watermelon.png"))  # встановлюємо іконку кнопки (зображення арбуза)
        self.button.setIconSize(QSize(200, 200))  # задаємо розмір іконки (200x200 пікселів)
        self.button.setFixedSize(220, 220)  # задаємо розмір самої кнопки, щоб вона була трохи більша за іконку
        self.button.clicked.connect(self.increase_count)  # підключаємо метод, який викликається при кліку на кнопку

        layout.addWidget(self.button)  # додаємо кнопку до layout'у

        self.setLayout(layout)  # встановлюємо наш layout у головне вікно

    # Метод, який збільшує лічильник кліків і оновлює текст
    def increase_count(self):
        self.click_count += 1  # збільшуємо лічильник на 1
        self.label.setText(f"Кількість кліків: {self.click_count}")  # оновлюємо текст в label

# Якщо цей файл запущено напряму, запускаємо програму
if __name__ == "__main__":
    app = QApplication(sys.argv)  # створюємо об’єкт програми
    window = WatermelonClicker()  # створюємо наше головне вікно
    window.show()  # показуємо вікно
    sys.exit(app.exec_())  # запускаємо цикл обробки подій і чекаємо закриття вікна