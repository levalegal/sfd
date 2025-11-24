from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
                             QTableWidgetItem, QPushButton, QDialog, QFormLayout, 
                             QLineEdit, QComboBox, QMessageBox, QLabel)
from PyQt6.QtCore import Qt
from app.models import StudentModel
from app.utils.logger import setup_logger
from app.utils.export import export_students_to_csv
from PyQt6.QtWidgets import QFileDialog

logger = setup_logger('students_window')


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
                logger.info(f"Обновлен студент ID: {self.student_id}")
            else:
                student_id = self.model.create(surname, name, patronymic, gender, phone, email, group)
                logger.info(f"Создан студент ID: {student_id}")
            self.accept()
        except ValueError as e:
            logger.warning(f"Ошибка валидации: {e}")
            QMessageBox.warning(self, 'Ошибка валидации', str(e))
        except Exception as e:
            logger.error(f"Ошибка сохранения студента: {e}")
            QMessageBox.critical(self, 'Ошибка', f'Ошибка сохранения: {str(e)}')


class StudentsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.model = StudentModel()
        self.init_ui()
        self.load_data()
    
    def init_ui(self):
        self.setWindowTitle('👥 Управление студентами')
        self.setMinimumSize(1000, 650)
        
        layout = QVBoxLayout()
        
        # Поиск
        search_layout = QHBoxLayout()
        search_label = QLabel('🔍 Поиск:')
        search_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: 600;
                color: #34495e;
                padding: 5px;
            }
        """)
        self.search_edit = QLineEdit()
        self.search_edit.setObjectName("search")
        self.search_edit.setPlaceholderText('Введите фамилию, имя или группу...')
        self.search_edit.textChanged.connect(self.filter_data)
        self.search_edit.setStyleSheet("""
            QLineEdit#search {
                padding: 12px 16px;
                font-size: 14px;
                border: 2px solid #3498db;
                border-radius: 25px;
                background-color: white;
            }
            QLineEdit#search:focus {
                border: 2px solid #2980b9;
                background-color: #f8f9fa;
            }
        """)
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_edit)
        
        # Кнопки управления
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        
        self.add_btn = QPushButton('➕ Добавить')
        self.edit_btn = QPushButton('✏️ Редактировать')
        self.delete_btn = QPushButton('🗑️ Удалить')
        self.export_btn = QPushButton('📥 Экспорт в CSV')
        self.refresh_btn = QPushButton('🔄 Обновить')
        
        # Стили для кнопок
        self.add_btn.setProperty("class", "action")
        self.edit_btn.setProperty("class", "action")
        self.delete_btn.setProperty("class", "danger")
        self.export_btn.setProperty("class", "action")
        self.refresh_btn.setProperty("class", "action")
        
        self.add_btn.clicked.connect(self.add_student)
        self.edit_btn.clicked.connect(self.edit_student)
        self.delete_btn.clicked.connect(self.delete_student)
        self.export_btn.clicked.connect(self.export_data)
        self.refresh_btn.clicked.connect(self.load_data)
        
        buttons_layout.addWidget(self.add_btn)
        buttons_layout.addWidget(self.edit_btn)
        buttons_layout.addWidget(self.delete_btn)
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.export_btn)
        buttons_layout.addWidget(self.refresh_btn)
        
        # Таблица
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            'ID', 'Фамилия', 'Имя', 'Отчество', 'Пол', 'Телефон', 'Email', 'Группа'
        ])
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(True)
        
        # Статус
        self.status_label = QLabel('Всего студентов: 0')
        self.status_label.setObjectName("status")
        self.status_label.setStyleSheet("""
            QLabel#status {
                background-color: #ecf0f1;
                padding: 10px 16px;
                border-radius: 6px;
                color: #34495e;
                font-size: 13px;
                font-weight: 600;
                border-left: 4px solid #3498db;
            }
        """)
        
        layout.addLayout(search_layout)
        layout.addLayout(buttons_layout)
        layout.addWidget(self.table)
        layout.addWidget(self.status_label)
        self.setLayout(layout)
    
    def load_data(self):
        try:
            students = self.model.get_all()
            self.all_students = students
            self.filter_data()
            logger.info(f"Загружено {len(students)} студентов")
        except Exception as e:
            logger.error(f"Ошибка загрузки данных: {e}")
            QMessageBox.critical(self, 'Ошибка', f'Ошибка загрузки данных: {str(e)}')
    
    def filter_data(self):
        """Фильтрация данных по поисковому запросу"""
        if not hasattr(self, 'all_students'):
            return
        
        search_text = self.search_edit.text().lower().strip()
        
        if search_text:
            filtered = [
                s for s in self.all_students
                if (search_text in str(s[1]).lower() or  # фамилия
                    search_text in str(s[2]).lower() or  # имя
                    search_text in str(s[7]).lower())    # группа
            ]
        else:
            filtered = self.all_students
        
        self.table.setRowCount(len(filtered))
        
        for row, student in enumerate(filtered):
            for col, value in enumerate(student):
                item = QTableWidgetItem(str(value) if value is not None else '')
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.table.setItem(row, col, item)
        
        self.table.resizeColumnsToContents()
        self.status_label.setText(f'Всего студентов: {len(filtered)} / {len(self.all_students)}')
    
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
                logger.info(f"Удален студент ID: {student_id}")
                self.load_data()
                QMessageBox.information(self, 'Успех', 'Студент удален')
            except ValueError as e:
                logger.warning(f"Нельзя удалить студента ID {student_id}: {e}")
                QMessageBox.warning(self, 'Ошибка', str(e))
            except Exception as e:
                logger.error(f"Ошибка удаления студента: {e}")
                QMessageBox.critical(self, 'Ошибка', f'Ошибка удаления: {str(e)}')
    
    def export_data(self):
        """Экспорт данных в CSV"""
        if not hasattr(self, 'all_students') or not self.all_students:
            QMessageBox.warning(self, 'Предупреждение', 'Нет данных для экспорта')
            return
        
        filename, _ = QFileDialog.getSaveFileName(
            self, 'Сохранить как CSV', 'students_export.csv', 'CSV Files (*.csv)'
        )
        
        if filename:
            try:
                export_students_to_csv(self.all_students, filename)
                QMessageBox.information(self, 'Успех', f'Данные экспортированы в {filename}')
            except Exception as e:
                logger.error(f"Ошибка экспорта: {e}")
                QMessageBox.critical(self, 'Ошибка', f'Ошибка экспорта: {str(e)}')

