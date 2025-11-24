"""
Стили для приложения
"""

APP_STYLE = """
QMainWindow {
    background-color: #f5f5f5;
}

QPushButton {
    background-color: #4CAF50;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    font-size: 12px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #45a049;
}

QPushButton:pressed {
    background-color: #3d8b40;
}

QPushButton:disabled {
    background-color: #cccccc;
    color: #666666;
}

QTableWidget {
    background-color: white;
    alternate-background-color: #f9f9f9;
    selection-background-color: #e3f2fd;
    border: 1px solid #ddd;
    gridline-color: #e0e0e0;
}

QTableWidget::item {
    padding: 5px;
}

QTableWidget::item:selected {
    background-color: #e3f2fd;
    color: #1976d2;
}

QHeaderView::section {
    background-color: #2196F3;
    color: white;
    padding: 8px;
    border: none;
    font-weight: bold;
}

QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QDateEdit {
    padding: 6px;
    border: 1px solid #ddd;
    border-radius: 4px;
    background-color: white;
    font-size: 12px;
}

QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus, QDateEdit:focus {
    border: 2px solid #2196F3;
}

QDialog {
    background-color: white;
}

QLabel {
    color: #333;
    font-size: 12px;
}

QMessageBox {
    background-color: white;
}
"""

