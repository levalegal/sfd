from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
                             QTableWidgetItem, QPushButton, QDialog, QFormLayout, 
                             QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox, QMessageBox)
from PyQt6.QtCore import Qt
from app.models import RoomModel, BuildingModel


class RoomDialog(QDialog):
    def __init__(self, parent=None, room_id=None):
        super().__init__(parent)
        self.room_id = room_id
        self.room_model = RoomModel()
        self.building_model = BuildingModel()
        self.init_ui()
        
        if room_id:
            self.load_room()
    
    def init_ui(self):
        self.setWindowTitle('Редактировать комнату' if self.room_id else 'Добавить комнату')
        self.setMinimumWidth(400)
        
        layout = QFormLayout()
        
        self.building_combo = QComboBox()
        self.floor_spin = QSpinBox()
        self.floor_spin.setMinimum(1)
        self.floor_spin.setMaximum(100)
        self.room_number_edit = QLineEdit()
        self.capacity_spin = QSpinBox()
        self.capacity_spin.setMinimum(1)
        self.capacity_spin.setMaximum(20)
        self.area_spin = QDoubleSpinBox()
        self.area_spin.setMinimum(0)
        self.area_spin.setMaximum(1000)
        self.area_spin.setDecimals(2)
        self.area_spin.setSuffix(' м²')
        
        # Загрузка корпусов
        self.load_buildings()
        self.building_combo.currentIndexChanged.connect(self.update_floors)
        
        layout.addRow('Корпус*:', self.building_combo)
        layout.addRow('Этаж*:', self.floor_spin)
        layout.addRow('Номер комнаты*:', self.room_number_edit)
        layout.addRow('Вместимость*:', self.capacity_spin)
        layout.addRow('Площадь:', self.area_spin)
        
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
    
    def load_buildings(self):
        buildings = self.building_model.get_all()
        self.building_combo.clear()
        for building in buildings:
            self.building_combo.addItem(f"{building[1]} - {building[2]}", building[0])
    
    def update_floors(self):
        building_id = self.building_combo.currentData()
        if building_id:
            building = self.building_model.get_by_id(building_id)
            if building:
                self.floor_spin.setMaximum(building[3])
    
    def load_room(self):
        room = self.room_model.get_by_id(self.room_id)
        if room:
            # room format: (id, building_id, floor, room_number, capacity, area, building_number, address)
            building_id = room[1]
            for i in range(self.building_combo.count()):
                if self.building_combo.itemData(i) == building_id:
                    self.building_combo.setCurrentIndex(i)
                    break
            self.floor_spin.setValue(room[2])
            self.room_number_edit.setText(room[3])
            self.capacity_spin.setValue(room[4])
            if room[5]:
                self.area_spin.setValue(room[5])
    
    def save(self):
        building_id = self.building_combo.currentData()
        floor = self.floor_spin.value()
        room_number = self.room_number_edit.text().strip()
        capacity = self.capacity_spin.value()
        area = self.area_spin.value() if self.area_spin.value() > 0 else None
        
        if not building_id or not room_number:
            QMessageBox.warning(self, 'Ошибка', 'Заполните все обязательные поля')
            return
        
        try:
            if self.room_id:
                self.room_model.update(self.room_id, building_id, floor, room_number, capacity, area)
            else:
                self.room_model.create(building_id, floor, room_number, capacity, area)
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', str(e))


class RoomsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.model = RoomModel()
        self.init_ui()
        self.load_data()
    
    def init_ui(self):
        self.setWindowTitle('Управление комнатами')
        self.setMinimumSize(900, 600)
        
        layout = QVBoxLayout()
        
        # Кнопки управления
        buttons_layout = QHBoxLayout()
        self.add_btn = QPushButton('Добавить')
        self.edit_btn = QPushButton('Редактировать')
        self.delete_btn = QPushButton('Удалить')
        self.refresh_btn = QPushButton('Обновить')
        
        self.add_btn.clicked.connect(self.add_room)
        self.edit_btn.clicked.connect(self.edit_room)
        self.delete_btn.clicked.connect(self.delete_room)
        self.refresh_btn.clicked.connect(self.load_data)
        
        buttons_layout.addWidget(self.add_btn)
        buttons_layout.addWidget(self.edit_btn)
        buttons_layout.addWidget(self.delete_btn)
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.refresh_btn)
        
        # Таблица
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            'ID', 'Корпус', 'Адрес', 'Этаж', 'Номер комнаты', 'Вместимость', 'Площадь'
        ])
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        
        layout.addLayout(buttons_layout)
        layout.addWidget(self.table)
        self.setLayout(layout)
    
    def load_data(self):
        rooms = self.model.get_all()
        self.table.setRowCount(len(rooms))
        
        for row, room in enumerate(rooms):
            # room format: (id, building_id, floor, room_number, capacity, area, building_number, address)
            self.table.setItem(row, 0, QTableWidgetItem(str(room[0])))
            self.table.setItem(row, 1, QTableWidgetItem(str(room[6])))
            self.table.setItem(row, 2, QTableWidgetItem(str(room[7])))
            self.table.setItem(row, 3, QTableWidgetItem(str(room[2])))
            self.table.setItem(row, 4, QTableWidgetItem(str(room[3])))
            self.table.setItem(row, 5, QTableWidgetItem(str(room[4])))
            area_text = f"{room[5]:.2f}" if room[5] else ""
            self.table.setItem(row, 6, QTableWidgetItem(area_text))
            
            for col in range(7):
                item = self.table.item(row, col)
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        
        self.table.resizeColumnsToContents()
    
    def add_room(self):
        dialog = RoomDialog(self)
        if dialog.exec():
            self.load_data()
    
    def edit_room(self):
        selected = self.table.selectedItems()
        if not selected:
            QMessageBox.warning(self, 'Предупреждение', 'Выберите комнату для редактирования')
            return
        
        room_id = int(self.table.item(selected[0].row(), 0).text())
        dialog = RoomDialog(self, room_id)
        if dialog.exec():
            self.load_data()
    
    def delete_room(self):
        selected = self.table.selectedItems()
        if not selected:
            QMessageBox.warning(self, 'Предупреждение', 'Выберите комнату для удаления')
            return
        
        room_id = int(self.table.item(selected[0].row(), 0).text())
        
        reply = QMessageBox.question(
            self, 'Подтверждение', 
            'Вы уверены, что хотите удалить эту комнату?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.model.delete(room_id)
                self.load_data()
                QMessageBox.information(self, 'Успех', 'Комната удалена')
            except ValueError as e:
                QMessageBox.warning(self, 'Ошибка', str(e))

