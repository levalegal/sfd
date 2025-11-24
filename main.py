"""
Главный файл приложения
Информационная система управления студенческим общежитием
"""
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QStackedWidget
from PyQt6.QtCore import Qt
from app.ui.students_window import StudentsWindow
from app.ui.commandants_window import CommandantsWindow
from app.ui.buildings_window import BuildingsWindow
from app.ui.rooms_window import RoomsWindow
from app.ui.checkin_window import CheckinWindow
from app.ui.checkout_window import CheckoutWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('Информационная система управления студенческим общежитием')
        self.setMinimumSize(1200, 700)
        
        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Основной layout
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Боковая панель с кнопками
        sidebar = QWidget()
        sidebar.setFixedWidth(200)
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        self.students_btn = QPushButton('Студенты')
        self.commandants_btn = QPushButton('Коменданты')
        self.buildings_btn = QPushButton('Корпуса')
        self.rooms_btn = QPushButton('Комнаты')
        self.checkin_btn = QPushButton('Заселения')
        self.checkout_btn = QPushButton('Выселения')
        
        self.students_btn.clicked.connect(lambda: self.show_window(0))
        self.commandants_btn.clicked.connect(lambda: self.show_window(1))
        self.buildings_btn.clicked.connect(lambda: self.show_window(2))
        self.rooms_btn.clicked.connect(lambda: self.show_window(3))
        self.checkin_btn.clicked.connect(lambda: self.show_window(4))
        self.checkout_btn.clicked.connect(lambda: self.show_window(5))
        
        sidebar_layout.addWidget(self.students_btn)
        sidebar_layout.addWidget(self.commandants_btn)
        sidebar_layout.addWidget(self.buildings_btn)
        sidebar_layout.addWidget(self.rooms_btn)
        sidebar_layout.addWidget(self.checkin_btn)
        sidebar_layout.addWidget(self.checkout_btn)
        sidebar_layout.addStretch()
        
        sidebar.setLayout(sidebar_layout)
        
        # Stacked widget для окон
        self.stacked_widget = QStackedWidget()
        
        # Создание окон
        self.students_window = StudentsWindow()
        self.commandants_window = CommandantsWindow()
        self.buildings_window = BuildingsWindow()
        self.rooms_window = RoomsWindow()
        self.checkin_window = CheckinWindow()
        self.checkout_window = CheckoutWindow()
        
        self.stacked_widget.addWidget(self.students_window)
        self.stacked_widget.addWidget(self.commandants_window)
        self.stacked_widget.addWidget(self.buildings_window)
        self.stacked_widget.addWidget(self.rooms_window)
        self.stacked_widget.addWidget(self.checkin_window)
        self.stacked_widget.addWidget(self.checkout_window)
        
        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.stacked_widget)
        
        # Показать первое окно
        self.show_window(0)
    
    def show_window(self, index):
        self.stacked_widget.setCurrentIndex(index)
        
        # Обновить данные при переключении
        if index == 0:
            self.students_window.load_data()
        elif index == 1:
            self.commandants_window.load_data()
        elif index == 2:
            self.buildings_window.load_data()
        elif index == 3:
            self.rooms_window.load_data()
        elif index == 4:
            self.checkin_window.load_data()
        elif index == 5:
            self.checkout_window.load_data()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
