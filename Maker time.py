import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QPushButton,
    QMessageBox, QSpacerItem, QSizePolicy
)
from PyQt5.QtGui import QIcon, QFont, QPalette, QBrush, QPixmap
from PyQt5.QtCore import QSize, QTimer, Qt


class WatermelonClicker(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🍉 Арбуз Клікер Deluxe")
        self.setFixedSize(400, 650)

        # Змінні гри
        self.click_count = 0
        self.click_multiplier = 1
        self.upgrade_cost = 10

        self.autoclicker_enabled = False
        self.autoclicker_cost = 50

        self.super_click_active = False
        self.super_click_cost = 100
        self.super_click_multiplier = 10
        self.super_click_duration = 10000  # мілісекунд (10 сек)

        self.set_background("background.jpg")

        # Layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Spacer для центрування
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Лічильник кліків
        self.label = QLabel("Кількість кліків: 0")
        self.label.setFont(QFont("Comic Sans MS", 18))
        self.label.setStyleSheet("color: white;")
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        # Множник
        self.multiplier_label = QLabel("Множник кліків: x1")
        self.multiplier_label.setFont(QFont("Comic Sans MS", 14))
        self.multiplier_label.setStyleSheet("color: lightgreen;")
        self.multiplier_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.multiplier_label)

        # Кнопка арбуза
        self.button = QPushButton()
        self.button.setIcon(QIcon("watermelon.png"))
        self.button.setIconSize(QSize(200, 200))
        self.button.setFixedSize(220, 220)
        self.button.setStyleSheet("""
            QPushButton {
                border: 4px solid #55aa55;
                border-radius: 20px;
                background-color: #e0ffe0;
            }
            QPushButton:hover {
                background-color: #c6f7c6;
            }
        """)
        self.button.clicked.connect(self.increase_count)
        layout.addWidget(self.button, alignment=Qt.AlignCenter)

        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Кнопка апгрейду
        self.upgrade_button = QPushButton("🔼 Купити апгрейд — 10 кліків")
        self.upgrade_button.setFont(QFont("Verdana", 12))
        self.upgrade_button.setStyleSheet(self.get_button_style())
        self.upgrade_button.clicked.connect(self.buy_upgrade)
        layout.addWidget(self.upgrade_button, alignment=Qt.AlignCenter)

        # Кнопка автокліку
        self.autoclicker_button = QPushButton("🤖 Купити автоклік — 50 кліків")
        self.autoclicker_button.setFont(QFont("Verdana", 12))
        self.autoclicker_button.setStyleSheet(self.get_button_style())
        self.autoclicker_button.clicked.connect(self.buy_autoclicker)
        layout.addWidget(self.autoclicker_button, alignment=Qt.AlignCenter)

        # Кнопка супер кліку
        self.super_click_button = QPushButton("💥 Супер Клік — 100 кліків")
        self.super_click_button.setFont(QFont("Verdana", 12))
        self.super_click_button.setStyleSheet(self.get_button_style())
        self.super_click_button.clicked.connect(self.activate_super_click)
        layout.addWidget(self.super_click_button, alignment=Qt.AlignCenter)

        # Таймери
        self.autoclicker_timer = QTimer()
        self.autoclicker_timer.timeout.connect(self.auto_click)

        self.super_click_timer = QTimer()
        self.super_click_timer.setSingleShot(True)
        self.super_click_timer.timeout.connect(self.deactivate_super_click)

        self.setLayout(layout)

    def set_background(self, image_path):
        """Встановлює фон"""
        self.setAutoFillBackground(True)
        palette = QPalette()
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            self.setStyleSheet("background-color: #2e2e2e;")
        else:
            scaled = pixmap.scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
            palette.setBrush(QPalette.Window, QBrush(scaled))
            self.setPalette(palette)

    def get_button_style(self):
        """Стилі кнопок"""
        return """
            QPushButton {
                background-color: #a2d5ab;
                color: black;
                padding: 10px;
                border-radius: 10px;
                border: 2px solid #4caf50;
            }
            QPushButton:hover {
                background-color: #90c99f;
            }
        """

    def increase_count(self):
        # Визначаємо множник
        multiplier = self.click_multiplier
        if self.super_click_active:
            multiplier *= self.super_click_multiplier

        self.click_count += multiplier
        self.label.setText(f"Кількість кліків: {self.click_count}")

        # Анімація натискання
        self.button.setIconSize(QSize(180, 180))
        QTimer.singleShot(100, lambda: self.button.setIconSize(QSize(200, 200)))

    def buy_upgrade(self):
        if self.click_count >= self.upgrade_cost:
            self.click_count -= self.upgrade_cost
            self.click_multiplier += 1
            self.upgrade_cost *= 2
            self.label.setText(f"Кількість кліків: {self.click_count}")
            self.multiplier_label.setText(f"Множник кліків: x{self.click_multiplier}")
            self.upgrade_button.setText(f"🔼 Купити апгрейд — {self.upgrade_cost} кліків")
        else:
            QMessageBox.warning(self, "Недостатньо кліків", "Не вистачає кліків для апгрейду!")

    def buy_autoclicker(self):
        if self.autoclicker_enabled:
            QMessageBox.information(self, "Автоклік активний", "Автоклік уже працює.")
            return
        if self.click_count >= self.autoclicker_cost:
            self.click_count -= self.autoclicker_cost
            self.label.setText(f"Кількість кліків: {self.click_count}")
            self.autoclicker_enabled = True
            self.autoclicker_timer.start(1000)
            self.autoclicker_button.setText("✅ Автоклік активовано")
            self.autoclicker_button.setEnabled(False)
        else:
            QMessageBox.warning(self, "Недостатньо кліків", "Не вистачає кліків для автокліку!")

    def auto_click(self):
        multiplier = self.click_multiplier
        if self.super_click_active:
            multiplier *= self.super_click_multiplier
        self.click_count += multiplier
        self.label.setText(f"Кількість кліків: {self.click_count}")

    def activate_super_click(self):
        if self.super_click_active:
            QMessageBox.information(self, "Уже активовано", "Супер Клік уже активний!")
            return
        if self.click_count >= self.super_click_cost:
            self.click_count -= self.super_click_cost
            self.super_click_active = True
            self.label.setText(f"Кількість кліків: {self.click_count}")
            self.super_click_button.setText("💥 Супер Клік активовано!")
            self.super_click_button.setEnabled(False)
            self.super_click_timer.start(self.super_click_duration)
        else:
            QMessageBox.warning(self, "Недостатньо кліків", "Не вистачає кліків для Супер Кліку!")

    def deactivate_super_click(self):
        self.super_click_active = False
        self.super_click_button.setText(f"💥 Супер Клік — {self.super_click_cost} кліків")
        self.super_click_button.setEnabled(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WatermelonClicker()
    window.show()
    sys.exit(app.exec_())
