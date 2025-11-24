from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
                             QTableWidgetItem, QPushButton, QDialog, QFormLayout, 
                             QLineEdit, QComboBox, QDateEdit, QMessageBox, QLabel)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont
from app.models import CheckinModel, StudentModel, CommandantModel, RoomModel


class CheckinDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.checkin_model = CheckinModel()
        self.student_model = StudentModel()
        self.commandant_model = CommandantModel()
        self.room_model = RoomModel()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('Заселение студента')
        self.setMinimumWidth(500)
        
        layout = QFormLayout()
        
        # Студент
        student_label = QLabel('Данные студента')
        student_label.setFont(QFont('Arial', 10, QFont.Weight.Bold))
        layout.addRow(student_label)
        
        self.student_combo = QComboBox()
        self.load_students()
        layout.addRow('Студент*:', self.student_combo)
        
        # Комендант
        commandant_label = QLabel('Данные коменданта')
        commandant_label.setFont(QFont('Arial', 10, QFont.Weight.Bold))
        layout.addRow(commandant_label)
        
        self.commandant_combo = QComboBox()
        self.load_commandants()
        layout.addRow('Комендант*:', self.commandant_combo)
        
        # Комната
        room_label = QLabel('Данные комнаты')
        room_label.setFont(QFont('Arial', 10, QFont.Weight.Bold))
        layout.addRow(room_label)
        
        self.room_combo = QComboBox()
        self.load_rooms()
        layout.addRow('Комната*:', self.room_combo)
        
        # Дата
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        layout.addRow('Дата заселения*:', self.date_edit)
        
        buttons = QHBoxLayout()
        save_btn = QPushButton('Заселить')
        cancel_btn = QPushButton('Отмена')
        save_btn.clicked.connect(self.save)
        cancel_btn.clicked.connect(self.reject)
        buttons.addWidget(save_btn)
        buttons.addWidget(cancel_btn)
        
        main_layout = QVBoxLayout()
        main_layout.addLayout(layout)
        main_layout.addLayout(buttons)
        self.setLayout(main_layout)
    
    def load_students(self):
        students = self.student_model.get_all()
        self.student_combo.clear()
        for student in students:
            name = f"{student[1]} {student[2]} {student[3] or ''}".strip()
            self.student_combo.addItem(name, student[0])
    
    def load_commandants(self):
        commandants = self.commandant_model.get_all()
        self.commandant_combo.clear()
        for commandant in commandants:
            name = f"{commandant[1]} {commandant[2]} {commandant[3] or ''}".strip()
            self.commandant_combo.addItem(name, commandant[0])
    
    def load_rooms(self):
        rooms = self.room_model.get_all()
        self.room_combo.clear()
        for room in rooms:
            # room format: (id, building_id, floor, room_number, capacity, area, building_number, address)
            room_text = f"Корпус {room[6]}, {room[7]}, этаж {room[2]}, комната {room[3]}"
            self.room_combo.addItem(room_text, room[0])
    
    def save(self):
        student_id = self.student_combo.currentData()
        commandant_id = self.commandant_combo.currentData()
        room_id = self.room_combo.currentData()
        checkin_date = self.date_edit.date().toString('yyyy-MM-dd')
        
        if not student_id or not commandant_id or not room_id:
            QMessageBox.warning(self, 'Ошибка', 'Заполните все обязательные поля')
            return
        
        try:
            self.checkin_model.create(student_id, commandant_id, room_id, checkin_date)
            QMessageBox.information(self, 'Успех', 'Студент успешно заселен')
            self.accept()
        except ValueError as e:
            QMessageBox.warning(self, 'Ошибка заселения', str(e))
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', str(e))


class CheckinWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.model = CheckinModel()
        self.init_ui()
        self.load_data()
    
    def init_ui(self):
        self.setWindowTitle('Заселения')
        self.setMinimumSize(1000, 600)
        
        layout = QVBoxLayout()
        
        # Кнопки управления
        buttons_layout = QHBoxLayout()
        self.add_btn = QPushButton('Новое заселение')
        self.refresh_btn = QPushButton('Обновить')
        
        self.add_btn.clicked.connect(self.add_checkin)
        self.refresh_btn.clicked.connect(self.load_data)
        
        buttons_layout.addWidget(self.add_btn)
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.refresh_btn)
        
        # Таблица
        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels([
            'ID', 'Студент', 'Комендант', 'Корпус', 'Адрес', 'Этаж', 'Комната', 'Дата заселения'
        ])
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        
        layout.addLayout(buttons_layout)
        layout.addWidget(self.table)
        self.setLayout(layout)
    
    def load_data(self):
        checkins = self.model.get_all()
        self.table.setRowCount(len(checkins))
        
        for row, checkin in enumerate(checkins):
            # checkin format: (id, student_id, commandant_id, room_id, checkin_date, 
            #                  student_name, commandant_name, room_number, floor, building_number, address)
            self.table.setItem(row, 0, QTableWidgetItem(str(checkin[0])))
            self.table.setItem(row, 1, QTableWidgetItem(str(checkin[5])))
            self.table.setItem(row, 2, QTableWidgetItem(str(checkin[6])))
            self.table.setItem(row, 3, QTableWidgetItem(str(checkin[9])))
            self.table.setItem(row, 4, QTableWidgetItem(str(checkin[10])))
            self.table.setItem(row, 5, QTableWidgetItem(str(checkin[8])))
            self.table.setItem(row, 6, QTableWidgetItem(str(checkin[7])))
            self.table.setItem(row, 7, QTableWidgetItem(str(checkin[4])))
            
            for col in range(8):
                item = self.table.item(row, col)
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        
        self.table.resizeColumnsToContents()

    def add_checkin(self):
        dialog = CheckinDialog(self)
        if dialog.exec():
            self.load_data()

