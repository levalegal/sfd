from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
                             QTableWidgetItem, QPushButton, QDialog, QFormLayout, 
                             QLineEdit, QComboBox, QMessageBox, QLabel)
from PyQt6.QtCore import Qt
from app.models import StudentModel


class StudentDialog(QDialog):
    def __init__(self, parent=None, student_id=None):
        super().__init__(parent)
        self.student_id = student_id
        self.model = StudentModel()
        self.init_ui()
        
        if student_id:
            self.load_student()
    
    def init_ui(self):
        self.setWindowTitle('Редактировать студента' if self.student_id else 'Добавить студента')
        self.setMinimumWidth(400)
        
        layout = QFormLayout()
        
        self.surname_edit = QLineEdit()
        self.name_edit = QLineEdit()
        self.patronymic_edit = QLineEdit()
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(['М', 'Ж'])
        self.phone_edit = QLineEdit()
        self.email_edit = QLineEdit()
        self.group_edit = QLineEdit()
        
        layout.addRow('Фамилия*:', self.surname_edit)
        layout.addRow('Имя*:', self.name_edit)
        layout.addRow('Отчество:', self.patronymic_edit)
        layout.addRow('Пол*:', self.gender_combo)
        layout.addRow('Телефон*:', self.phone_edit)
        layout.addRow('Email:', self.email_edit)
        layout.addRow('Группа*:', self.group_edit)
        
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
    
    def load_student(self):
        student = self.model.get_by_id(self.student_id)
        if student:
            self.surname_edit.setText(student[1])
            self.name_edit.setText(student[2])
            self.patronymic_edit.setText(student[3] or '')
            self.gender_combo.setCurrentText(student[4])
            self.phone_edit.setText(student[5])
            self.email_edit.setText(student[6] or '')
            self.group_edit.setText(student[7])
    
    def save(self):
        surname = self.surname_edit.text().strip()
        name = self.name_edit.text().strip()
        patronymic = self.patronymic_edit.text().strip()
        gender = self.gender_combo.currentText()
        phone = self.phone_edit.text().strip()
        email = self.email_edit.text().strip()
        group = self.group_edit.text().strip()
        
        if not surname or not name or not phone or not group:
            QMessageBox.warning(self, 'Ошибка', 'Заполните все обязательные поля')
            return
        
        try:
            if self.student_id:
                self.model.update(self.student_id, surname, name, patronymic, gender, phone, email, group)
            else:
                self.model.create(surname, name, patronymic, gender, phone, email, group)
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', str(e))


class StudentsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.model = StudentModel()
        self.init_ui()
        self.load_data()
    
    def init_ui(self):
        self.setWindowTitle('Управление студентами')
        self.setMinimumSize(900, 600)
        
        layout = QVBoxLayout()
        
        # Кнопки управления
        buttons_layout = QHBoxLayout()
        self.add_btn = QPushButton('Добавить')
        self.edit_btn = QPushButton('Редактировать')
        self.delete_btn = QPushButton('Удалить')
        self.refresh_btn = QPushButton('Обновить')
        
        self.add_btn.clicked.connect(self.add_student)
        self.edit_btn.clicked.connect(self.edit_student)
        self.delete_btn.clicked.connect(self.delete_student)
        self.refresh_btn.clicked.connect(self.load_data)
        
        buttons_layout.addWidget(self.add_btn)
        buttons_layout.addWidget(self.edit_btn)
        buttons_layout.addWidget(self.delete_btn)
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.refresh_btn)
        
        # Таблица
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            'ID', 'Фамилия', 'Имя', 'Отчество', 'Пол', 'Телефон', 'Email', 'Группа'
        ])
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        
        layout.addLayout(buttons_layout)
        layout.addWidget(self.table)
        self.setLayout(layout)
    
    def load_data(self):
        students = self.model.get_all()
        self.table.setRowCount(len(students))
        
        for row, student in enumerate(students):
            for col, value in enumerate(student):
                item = QTableWidgetItem(str(value) if value is not None else '')
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.table.setItem(row, col, item)
        
        self.table.resizeColumnsToContents()
    
    def add_student(self):
        dialog = StudentDialog(self)
        if dialog.exec():
            self.load_data()
    
    def edit_student(self):
        selected = self.table.selectedItems()
        if not selected:
            QMessageBox.warning(self, 'Предупреждение', 'Выберите студента для редактирования')
            return
        
        student_id = int(self.table.item(selected[0].row(), 0).text())
        dialog = StudentDialog(self, student_id)
        if dialog.exec():
            self.load_data()
    
    def delete_student(self):
        selected = self.table.selectedItems()
        if not selected:
            QMessageBox.warning(self, 'Предупреждение', 'Выберите студента для удаления')
            return
        
        student_id = int(self.table.item(selected[0].row(), 0).text())
        
        reply = QMessageBox.question(
            self, 'Подтверждение', 
            'Вы уверены, что хотите удалить этого студента?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.model.delete(student_id)
                self.load_data()
                QMessageBox.information(self, 'Успех', 'Студент удален')
            except ValueError as e:
                QMessageBox.warning(self, 'Ошибка', str(e))

