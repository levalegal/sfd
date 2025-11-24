from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
                             QTableWidgetItem, QPushButton, QDialog, QFormLayout, 
                             QLineEdit, QSpinBox, QMessageBox, QLabel)
from PyQt6.QtCore import Qt
from app.models import BuildingModel


class BuildingDialog(QDialog):
    def __init__(self, parent=None, building_id=None):
        super().__init__(parent)
        self.building_id = building_id
        self.model = BuildingModel()
        self.init_ui()
        
        if building_id:
            self.load_building()
    
    def init_ui(self):
        self.setWindowTitle('Редактировать корпус' if self.building_id else 'Добавить корпус')
        self.setMinimumWidth(400)
        
        layout = QFormLayout()
        
        self.building_number_edit = QLineEdit()
        self.address_edit = QLineEdit()
        self.floors_spin = QSpinBox()
        self.floors_spin.setMinimum(1)
        self.floors_spin.setMaximum(100)
        
        layout.addRow('Номер корпуса*:', self.building_number_edit)
        layout.addRow('Адрес*:', self.address_edit)
        layout.addRow('Количество этажей*:', self.floors_spin)
        
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
    
    def load_building(self):
        building = self.model.get_by_id(self.building_id)
        if building:
            self.building_number_edit.setText(building[1])
            self.address_edit.setText(building[2])
            self.floors_spin.setValue(building[3])
    
    def save(self):
        building_number = self.building_number_edit.text().strip()
        address = self.address_edit.text().strip()
        floors_count = self.floors_spin.value()
        
        if not building_number or not address:
            QMessageBox.warning(self, 'Ошибка', 'Заполните все обязательные поля')
            return
        
        try:
            if self.building_id:
                self.model.update(self.building_id, building_number, address, floors_count)
            else:
                self.model.create(building_number, address, floors_count)
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', str(e))


class BuildingsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.model = BuildingModel()
        self.init_ui()
        self.load_data()
    
    def init_ui(self):
        self.setWindowTitle('Управление корпусами')
        self.setMinimumSize(800, 500)
        
        layout = QVBoxLayout()
        
        # Фильтр по адресу
        filter_layout = QHBoxLayout()
        filter_label = QLabel('Фильтр по адресу:')
        self.filter_edit = QLineEdit()
        self.filter_edit.setPlaceholderText('Введите адрес для поиска...')
        filter_btn = QPushButton('Применить фильтр')
        clear_filter_btn = QPushButton('Очистить')
        
        filter_btn.clicked.connect(self.apply_filter)
        clear_filter_btn.clicked.connect(self.clear_filter)
        self.filter_edit.returnPressed.connect(self.apply_filter)
        
        filter_layout.addWidget(filter_label)
        filter_layout.addWidget(self.filter_edit)
        filter_layout.addWidget(filter_btn)
        filter_layout.addWidget(clear_filter_btn)
        
        # Кнопки управления
        buttons_layout = QHBoxLayout()
        self.add_btn = QPushButton('Добавить')
        self.edit_btn = QPushButton('Редактировать')
        self.delete_btn = QPushButton('Удалить')
        self.refresh_btn = QPushButton('Обновить')
        
        self.add_btn.clicked.connect(self.add_building)
        self.edit_btn.clicked.connect(self.edit_building)
        self.delete_btn.clicked.connect(self.delete_building)
        self.refresh_btn.clicked.connect(self.load_data)
        
        buttons_layout.addWidget(self.add_btn)
        buttons_layout.addWidget(self.edit_btn)
        buttons_layout.addWidget(self.delete_btn)
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.refresh_btn)
        
        # Таблица
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels([
            'ID', 'Номер корпуса', 'Адрес', 'Этажей'
        ])
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        
        layout.addLayout(filter_layout)
        layout.addLayout(buttons_layout)
        layout.addWidget(self.table)
        self.setLayout(layout)
    
    def load_data(self, address_filter=None):
        buildings = self.model.get_all(address_filter)
        self.table.setRowCount(len(buildings))
        
        for row, building in enumerate(buildings):
            for col, value in enumerate(building):
                item = QTableWidgetItem(str(value) if value is not None else '')
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.table.setItem(row, col, item)
        
        self.table.resizeColumnsToContents()
    
    def apply_filter(self):
        filter_text = self.filter_edit.text().strip()
        self.load_data(filter_text if filter_text else None)
    
    def clear_filter(self):
        self.filter_edit.clear()
        self.load_data()
    
    def add_building(self):
        dialog = BuildingDialog(self)
        if dialog.exec():
            self.load_data()
    
    def edit_building(self):
        selected = self.table.selectedItems()
        if not selected:
            QMessageBox.warning(self, 'Предупреждение', 'Выберите корпус для редактирования')
            return
        
        building_id = int(self.table.item(selected[0].row(), 0).text())
        dialog = BuildingDialog(self, building_id)
        if dialog.exec():
            self.load_data()
    
    def delete_building(self):
        selected = self.table.selectedItems()
        if not selected:
            QMessageBox.warning(self, 'Предупреждение', 'Выберите корпус для удаления')
            return
        
        building_id = int(self.table.item(selected[0].row(), 0).text())
        
        reply = QMessageBox.question(
            self, 'Подтверждение', 
            'Вы уверены, что хотите удалить этот корпус?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.model.delete(building_id)
                self.load_data()
                QMessageBox.information(self, 'Успех', 'Корпус удален')
            except ValueError as e:
                QMessageBox.warning(self, 'Ошибка', str(e))

