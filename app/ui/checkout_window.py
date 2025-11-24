from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
                             QTableWidgetItem, QPushButton, QDialog, QFormLayout, 
                             QComboBox, QDateEdit, QMessageBox, QLabel)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont
from app.models import CheckoutModel, CheckinModel, CommandantModel


class CheckoutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.checkout_model = CheckoutModel()
        self.checkin_model = CheckinModel()
        self.commandant_model = CommandantModel()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('Выселение студента')
        self.setMinimumWidth(500)
        
        layout = QFormLayout()
        
        # Заселение
        checkin_label = QLabel('Данные заселения')
        checkin_label.setFont(QFont('Arial', 10, QFont.Weight.Bold))
        layout.addRow(checkin_label)
        
        self.checkin_combo = QComboBox()
        self.load_active_checkins()
        layout.addRow('Заселение*:', self.checkin_combo)
        
        # Комендант
        commandant_label = QLabel('Данные коменданта')
        commandant_label.setFont(QFont('Arial', 10, QFont.Weight.Bold))
        layout.addRow(commandant_label)
        
        self.commandant_combo = QComboBox()
        self.load_commandants()
        layout.addRow('Комендант*:', self.commandant_combo)
        
        # Дата
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        layout.addRow('Дата выселения*:', self.date_edit)
        
        buttons = QHBoxLayout()
        save_btn = QPushButton('Выселить')
        cancel_btn = QPushButton('Отмена')
        save_btn.clicked.connect(self.save)
        cancel_btn.clicked.connect(self.reject)
        buttons.addWidget(save_btn)
        buttons.addWidget(cancel_btn)
        
        main_layout = QVBoxLayout()
        main_layout.addLayout(layout)
        main_layout.addLayout(buttons)
        self.setLayout(main_layout)
    
    def load_active_checkins(self):
        checkins = self.checkin_model.get_active_checkins()
        self.checkin_combo.clear()
        for checkin in checkins:
            # checkin format: (id, student_id, commandant_id, room_id, checkin_date,
            #                  student_name, room_number, floor, building_number, address)
            checkin_text = f"{checkin[5]} - Корпус {checkin[8]}, этаж {checkin[7]}, комната {checkin[6]}"
            self.checkin_combo.addItem(checkin_text, checkin[0])
    
    def load_commandants(self):
        commandants = self.commandant_model.get_all()
        self.commandant_combo.clear()
        for commandant in commandants:
            name = f"{commandant[1]} {commandant[2]} {commandant[3] or ''}".strip()
            self.commandant_combo.addItem(name, commandant[0])
    
    def save(self):
        checkin_id = self.checkin_combo.currentData()
        commandant_id = self.commandant_combo.currentData()
        checkout_date = self.date_edit.date().toString('yyyy-MM-dd')
        
        if not checkin_id or not commandant_id:
            QMessageBox.warning(self, 'Ошибка', 'Заполните все обязательные поля')
            return
        
        try:
            self.checkout_model.create(checkin_id, commandant_id, checkout_date)
            QMessageBox.information(self, 'Успех', 'Студент успешно выселен')
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', str(e))


class CheckoutWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.model = CheckoutModel()
        self.init_ui()
        self.load_data()
    
    def init_ui(self):
        self.setWindowTitle('Выселения')
        self.setMinimumSize(1000, 600)
        
        layout = QVBoxLayout()
        
        # Кнопки управления
        buttons_layout = QHBoxLayout()
        self.add_btn = QPushButton('Новое выселение')
        self.refresh_btn = QPushButton('Обновить')
        
        self.add_btn.clicked.connect(self.add_checkout)
        self.refresh_btn.clicked.connect(self.load_data)
        
        buttons_layout.addWidget(self.add_btn)
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.refresh_btn)
        
        # Таблица
        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels([
            'ID', 'Студент', 'Комендант', 'Корпус', 'Адрес', 'Этаж', 'Комната', 'Дата выселения'
        ])
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        
        layout.addLayout(buttons_layout)
        layout.addWidget(self.table)
        self.setLayout(layout)
    
    def load_data(self):
        checkouts = self.model.get_all()
        self.table.setRowCount(len(checkouts))
        
        for row, checkout in enumerate(checkouts):
            # checkout format: (id, checkin_id, commandant_id, checkout_date,
            #                   student_name, commandant_name, room_number, floor, building_number, address)
            self.table.setItem(row, 0, QTableWidgetItem(str(checkout[0])))
            self.table.setItem(row, 1, QTableWidgetItem(str(checkout[4])))
            self.table.setItem(row, 2, QTableWidgetItem(str(checkout[5])))
            self.table.setItem(row, 3, QTableWidgetItem(str(checkout[8])))
            self.table.setItem(row, 4, QTableWidgetItem(str(checkout[9])))
            self.table.setItem(row, 5, QTableWidgetItem(str(checkout[7])))
            self.table.setItem(row, 6, QTableWidgetItem(str(checkout[6])))
            self.table.setItem(row, 7, QTableWidgetItem(str(checkout[3])))
            
            for col in range(8):
                item = self.table.item(row, col)
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        
        self.table.resizeColumnsToContents()

    def add_checkout(self):
        dialog = CheckoutDialog(self)
        if dialog.exec():
            self.load_data()

