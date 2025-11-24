from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
                             QTableWidgetItem, QPushButton, QDialog, QFormLayout, 
                             QLineEdit, QMessageBox, QLabel, QFileDialog)
from PyQt6.QtCore import Qt
from app.models import CommandantModel
from app.utils.logger import setup_logger
from app.utils.export import export_students_to_csv

logger = setup_logger('commandants_window')


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
        self.setMinimumWidth(450)
        self.setStyleSheet("""
            QDialog {
                background: white;
                border-radius: 12px;
            }
        """)
        
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(25, 25, 25, 25)
        
        # Заголовок
        title_label = QLabel('✏️ Редактировать коменданта' if self.commandant_id else '➕ Добавить коменданта')
        title_label.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                color: #2c3e50;
                padding-bottom: 10px;
                border-bottom: 2px solid #3498db;
            }
        """)
        main_layout.addWidget(title_label)
        
        layout = QFormLayout()
        layout.setSpacing(12)
        
        self.surname_edit = QLineEdit()
        self.name_edit = QLineEdit()
        self.patronymic_edit = QLineEdit()
        self.phone_edit = QLineEdit()
        
        # Стили для полей
        for edit in [self.surname_edit, self.name_edit, self.patronymic_edit, self.phone_edit]:
            edit.setStyleSheet("""
                QLineEdit {
                    padding: 10px 12px;
                    border: 2px solid #bdc3c7;
                    border-radius: 6px;
                    font-size: 13px;
                }
                QLineEdit:focus {
                    border: 2px solid #3498db;
                    background-color: #f8f9fa;
                }
            """)
        
        layout.addRow('Фамилия*:', self.surname_edit)
        layout.addRow('Имя*:', self.name_edit)
        layout.addRow('Отчество:', self.patronymic_edit)
        layout.addRow('Телефон*:', self.phone_edit)
        
        main_layout.addLayout(layout)
        
        buttons = QHBoxLayout()
        buttons.setSpacing(10)
        save_btn = QPushButton('💾 Сохранить')
        cancel_btn = QPushButton('❌ Отмена')
        save_btn.setProperty("class", "action")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background: #95a5a6;
                color: white;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: 600;
            }
            QPushButton:hover {
                background: #7f8c8d;
            }
        """)
        save_btn.clicked.connect(self.save)
        cancel_btn.clicked.connect(self.reject)
        buttons.addStretch()
        buttons.addWidget(save_btn)
        buttons.addWidget(cancel_btn)
        
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
                logger.info(f"Обновлен комендант ID: {self.commandant_id}")
            else:
                commandant_id = self.model.create(surname, name, patronymic, phone)
                logger.info(f"Создан комендант ID: {commandant_id}")
            self.accept()
        except ValueError as e:
            logger.warning(f"Ошибка валидации: {e}")
            QMessageBox.warning(self, 'Ошибка валидации', str(e))
        except Exception as e:
            logger.error(f"Ошибка сохранения коменданта: {e}")
            QMessageBox.critical(self, 'Ошибка', f'Ошибка сохранения: {str(e)}')


class CommandantsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.model = CommandantModel()
        self.init_ui()
        self.load_data()
    
    def init_ui(self):
        self.setWindowTitle('👮 Управление комендантами')
        self.setMinimumSize(900, 600)
        
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
        self.search_edit.setPlaceholderText('Введите фамилию или имя...')
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
        
        self.add_btn.setProperty("class", "action")
        self.edit_btn.setProperty("class", "action")
        self.delete_btn.setProperty("class", "danger")
        self.export_btn.setProperty("class", "action")
        self.refresh_btn.setProperty("class", "action")
        
        self.add_btn.clicked.connect(self.add_commandant)
        self.edit_btn.clicked.connect(self.edit_commandant)
        self.delete_btn.clicked.connect(self.delete_commandant)
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
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            'ID', 'Фамилия', 'Имя', 'Отчество', 'Телефон'
        ])
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(True)
        
        # Статус
        self.status_label = QLabel('Всего комендантов: 0')
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
            commandants = self.model.get_all()
            self.all_commandants = commandants
            self.filter_data()
            logger.info(f"Загружено {len(commandants)} комендантов")
        except Exception as e:
            logger.error(f"Ошибка загрузки данных: {e}")
            QMessageBox.critical(self, 'Ошибка', f'Ошибка загрузки данных: {str(e)}')
    
    def filter_data(self):
        """Фильтрация данных по поисковому запросу"""
        if not hasattr(self, 'all_commandants'):
            return
        
        search_text = self.search_edit.text().lower().strip()
        
        if search_text:
            filtered = [
                c for c in self.all_commandants
                if (search_text in str(c[1]).lower() or  # фамилия
                    search_text in str(c[2]).lower())    # имя
            ]
        else:
            filtered = self.all_commandants
        
        self.table.setRowCount(len(filtered))
        
        for row, commandant in enumerate(filtered):
            for col, value in enumerate(commandant):
                item = QTableWidgetItem(str(value) if value is not None else '')
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.table.setItem(row, col, item)
        
        self.table.resizeColumnsToContents()
        self.status_label.setText(f'Всего комендантов: {len(filtered)} / {len(self.all_commandants)}')
    
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
                logger.info(f"Удален комендант ID: {commandant_id}")
                self.load_data()
                QMessageBox.information(self, 'Успех', 'Комендант удален')
            except ValueError as e:
                logger.warning(f"Нельзя удалить коменданта ID {commandant_id}: {e}")
                QMessageBox.warning(self, 'Ошибка', str(e))
            except Exception as e:
                logger.error(f"Ошибка удаления коменданта: {e}")
                QMessageBox.critical(self, 'Ошибка', f'Ошибка удаления: {str(e)}')
    
    def export_data(self):
        """Экспорт данных в CSV"""
        if not hasattr(self, 'all_commandants') or not self.all_commandants:
            QMessageBox.warning(self, 'Предупреждение', 'Нет данных для экспорта')
            return
        
        filename, _ = QFileDialog.getSaveFileName(
            self, 'Сохранить как CSV', 'commandants_export.csv', 'CSV Files (*.csv)'
        )
        
        if filename:
            try:
                import csv
                with open(filename, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(['ID', 'Фамилия', 'Имя', 'Отчество', 'Телефон'])
                    for commandant in self.all_commandants:
                        writer.writerow(commandant)
                logger.info(f"Экспортировано {len(self.all_commandants)} комендантов")
                QMessageBox.information(self, 'Успех', f'Данные экспортированы в {filename}')
            except Exception as e:
                logger.error(f"Ошибка экспорта: {e}")
                QMessageBox.critical(self, 'Ошибка', f'Ошибка экспорта: {str(e)}')
