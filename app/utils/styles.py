"""
Современные стили для приложения
"""
APP_STYLE = """
/* Основное окно */
QMainWindow {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #f8f9fa, stop:1 #e9ecef);
}

/* Боковая панель */
QWidget#sidebar {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #2c3e50, stop:1 #34495e);
    border-right: 2px solid #1a252f;
}

/* Кнопки боковой панели */
QPushButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #3498db, stop:1 #2980b9);
    color: white;
    border: none;
    padding: 12px 20px;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 600;
    text-align: left;
    margin: 4px 8px;
    min-height: 40px;
}

QPushButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #5dade2, stop:1 #3498db);
    transform: translateX(5px);
}

QPushButton:pressed {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #2980b9, stop:1 #21618c);
}

QPushButton:disabled {
    background: #95a5a6;
    color: #7f8c8d;
}

/* Кнопки действий */
QPushButton[class="action"] {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #27ae60, stop:1 #229954);
    padding: 10px 18px;
    border-radius: 6px;
    font-size: 13px;
    font-weight: 600;
    min-width: 100px;
}

QPushButton[class="action"]:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #2ecc71, stop:1 #27ae60);
    box-shadow: 0 4px 8px rgba(39, 174, 96, 0.3);
}

QPushButton[class="action"]:pressed {
    background: #229954;
}

/* Кнопка удаления */
QPushButton[class="danger"] {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #e74c3c, stop:1 #c0392b);
}

QPushButton[class="danger"]:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #ec7063, stop:1 #e74c3c);
    box-shadow: 0 4px 8px rgba(231, 76, 60, 0.3);
}

/* Таблицы */
QTableWidget {
    background-color: white;
    alternate-background-color: #f8f9fa;
    selection-background-color: #d6eaf8;
    selection-color: #1a252f;
    border: 1px solid #dee2e6;
    border-radius: 8px;
    gridline-color: #e9ecef;
    font-size: 13px;
}

QTableWidget::item {
    padding: 10px;
    border-bottom: 1px solid #e9ecef;
}

QTableWidget::item:selected {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #d6eaf8, stop:1 #aed6f1);
    color: #1a252f;
    font-weight: 600;
}

QTableWidget::item:hover {
    background-color: #ebf5fb;
}

QHeaderView::section {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #34495e, stop:1 #2c3e50);
    color: white;
    padding: 12px 8px;
    border: none;
    font-weight: 700;
    font-size: 13px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    border-right: 1px solid #1a252f;
}

QHeaderView::section:first {
    border-top-left-radius: 8px;
}

QHeaderView::section:last {
    border-top-right-radius: 8px;
    border-right: none;
}

/* Поля ввода */
QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QDateEdit {
    padding: 10px 12px;
    border: 2px solid #bdc3c7;
    border-radius: 6px;
    background-color: white;
    font-size: 13px;
    color: #2c3e50;
    selection-background-color: #3498db;
    selection-color: white;
}

QLineEdit:focus, QComboBox:focus, QSpinBox:focus, 
QDoubleSpinBox:focus, QDateEdit:focus {
    border: 2px solid #3498db;
    background-color: #f8f9fa;
    outline: none;
}

QLineEdit:hover, QComboBox:hover, QSpinBox:hover,
QDoubleSpinBox:hover, QDateEdit:hover {
    border: 2px solid #95a5a6;
}

QComboBox::drop-down {
    border: none;
    width: 30px;
    background: #ecf0f1;
    border-top-right-radius: 6px;
    border-bottom-right-radius: 6px;
}

QComboBox::drop-down:hover {
    background: #d5dbdb;
}

QComboBox QAbstractItemView {
    background-color: white;
    selection-background-color: #3498db;
    selection-color: white;
    border: 1px solid #bdc3c7;
    border-radius: 4px;
}

/* Диалоги */
QDialog {
    background: white;
    border-radius: 12px;
}

QDialog QLabel {
    color: #2c3e50;
    font-size: 13px;
    font-weight: 500;
}

QDialog QLabel[class="title"] {
    font-size: 18px;
    font-weight: 700;
    color: #2c3e50;
    margin-bottom: 10px;
}

/* Формы */
QFormLayout {
    spacing: 15px;
}

QFormLayout QLabel {
    color: #34495e;
    font-weight: 600;
    font-size: 13px;
}

/* Сообщения */
QMessageBox {
    background-color: white;
    border-radius: 12px;
}

QMessageBox QLabel {
    color: #2c3e50;
    font-size: 14px;
    padding: 10px;
}

QMessageBox QPushButton {
    min-width: 100px;
    padding: 10px 20px;
    border-radius: 6px;
    font-weight: 600;
}

/* Поиск */
QLineEdit[class="search"] {
    padding: 12px 16px;
    font-size: 14px;
    border: 2px solid #3498db;
    border-radius: 25px;
    background-color: white;
}

QLineEdit[class="search"]:focus {
    border: 2px solid #2980b9;
    background-color: #f8f9fa;
}

/* Статус бар */
QLabel[class="status"] {
    background-color: #ecf0f1;
    padding: 8px 16px;
    border-radius: 4px;
    color: #34495e;
    font-size: 12px;
    font-weight: 600;
    border-left: 4px solid #3498db;
}

/* Виджеты */
QWidget {
    background-color: transparent;
}

/* Скроллбары */
QScrollBar:vertical {
    background: #ecf0f1;
    width: 12px;
    border-radius: 6px;
    margin: 0;
}

QScrollBar::handle:vertical {
    background: #95a5a6;
    border-radius: 6px;
    min-height: 20px;
    margin: 2px;
}

QScrollBar::handle:vertical:hover {
    background: #7f8c8d;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}

QScrollBar:horizontal {
    background: #ecf0f1;
    height: 12px;
    border-radius: 6px;
    margin: 0;
}

QScrollBar::handle:horizontal {
    background: #95a5a6;
    border-radius: 6px;
    min-width: 20px;
    margin: 2px;
}

QScrollBar::handle:horizontal:hover {
    background: #7f8c8d;
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0;
}
"""
