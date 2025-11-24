from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
                             QTableWidgetItem, QPushButton, QDialog, QFormLayout, 
                             QLineEdit, QMessageBox)
from PyQt6.QtCore import Qt
from app.models import CommandantModel


class CommandantDialog(QDialog):
    def __init__(self, parent=None, commandant_id=None):
        super().__init__(parent)
        self.commandant_id = commandant_id
        self.model = CommandantModel()
        self.init_ui()
        
        if commandant_id:
            self.load_commandant()
    
    def init_ui(self):
        self.setWindowTitle('Редактировать коменданта' if self.commandant_id else 'Добавить коменданта')
        self.setMinimumWidth(400)
        
        layout = QFormLayout()
        
        self.surname_edit = QLineEdit()
        self.name_edit = QLineEdit()
        self.patronymic_edit = QLineEdit()
        self.phone_edit = QLineEdit()
        
        layout.addRow('Фамилия*:', self.surname_edit)
        layout.addRow('Имя*:', self.name_edit)
        layout.addRow('Отчество:', self.patronymic_edit)
        layout.addRow('Телефон*:', self.phone_edit)
        
        buttons = QHBoxLayout()
        save_btn = QPushButton('Сохранить')
        cancel_btn = QPushButton('Отмена')
        save_btn.clicked.connect(self.save)
        cancel_btn.clicked.connect(self.reject)
        buttons.addWidget(save_btn)
        buttons.addWidget(cancel_btn)
        
        main_layout = QVBoxLayout()
        main_layout.addLayout(layout)
        main_layout.addLayout(buttons)
        self.setLayout(main_layout)
    
    def load_commandant(self):
        commandant = self.model.get_by_id(self.commandant_id)
        if commandant:
            self.surname_edit.setText(commandant[1])
            self.name_edit.setText(commandant[2])
            self.patronymic_edit.setText(commandant[3] or '')
            self.phone_edit.setText(commandant[4])
    
    def save(self):
        surname = self.surname_edit.text().strip()
        name = self.name_edit.text().strip()
        patronymic = self.patronymic_edit.text().strip()
        phone = self.phone_edit.text().strip()
        
        if not surname or not name or not phone:
            QMessageBox.warning(self, 'Ошибка', 'Заполните все обязательные поля')
            return
        
        try:
            if self.commandant_id:
                self.model.update(self.commandant_id, surname, name, patronymic, phone)
            else:
                self.model.create(surname, name, patronymic, phone)
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', str(e))


class CommandantsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.model = CommandantModel()
        self.init_ui()
        self.load_data()
    
    def init_ui(self):
        self.setWindowTitle('Управление комендантами')
        self.setMinimumSize(700, 500)
        
        layout = QVBoxLayout()
        
        # Кнопки управления
        buttons_layout = QHBoxLayout()
        self.add_btn = QPushButton('Добавить')
        self.edit_btn = QPushButton('Редактировать')
        self.delete_btn = QPushButton('Удалить')
        self.refresh_btn = QPushButton('Обновить')
        
        self.add_btn.clicked.connect(self.add_commandant)
        self.edit_btn.clicked.connect(self.edit_commandant)
        self.delete_btn.clicked.connect(self.delete_commandant)
        self.refresh_btn.clicked.connect(self.load_data)
        
        buttons_layout.addWidget(self.add_btn)
        buttons_layout.addWidget(self.edit_btn)
        buttons_layout.addWidget(self.delete_btn)
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.refresh_btn)
        
        # Таблица
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            'ID', 'Фамилия', 'Имя', 'Отчество', 'Телефон'
        ])
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        
        layout.addLayout(buttons_layout)
        layout.addWidget(self.table)
        self.setLayout(layout)
    
    def load_data(self):
        commandants = self.model.get_all()
        self.table.setRowCount(len(commandants))
        
        for row, commandant in enumerate(commandants):
            for col, value in enumerate(commandant):
                item = QTableWidgetItem(str(value) if value is not None else '')
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.table.setItem(row, col, item)
        
        self.table.resizeColumnsToContents()
    
    def add_commandant(self):
        dialog = CommandantDialog(self)
        if dialog.exec():
            self.load_data()
    
    def edit_commandant(self):
        selected = self.table.selectedItems()
        if not selected:
            QMessageBox.warning(self, 'Предупреждение', 'Выберите коменданта для редактирования')
            return
        
        commandant_id = int(self.table.item(selected[0].row(), 0).text())
        dialog = CommandantDialog(self, commandant_id)
        if dialog.exec():
            self.load_data()
    
    def delete_commandant(self):
        selected = self.table.selectedItems()
        if not selected:
            QMessageBox.warning(self, 'Предупреждение', 'Выберите коменданта для удаления')
            return
        
        commandant_id = int(self.table.item(selected[0].row(), 0).text())
        
        reply = QMessageBox.question(
            self, 'Подтверждение', 
            'Вы уверены, что хотите удалить этого коменданта?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.model.delete(commandant_id)
                self.load_data()
                QMessageBox.information(self, 'Успех', 'Комендант удален')
            except ValueError as e:
                QMessageBox.warning(self, 'Ошибка', str(e))

