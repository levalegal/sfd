"""
Окно дашборда со статистикой
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QGridLayout, QFrame)
from PyQt6.QtCore import Qt
from app.utils.statistics import Statistics
from app.utils.logger import setup_logger

logger = setup_logger('dashboard')


class DashboardWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.statistics = Statistics()
        self.init_ui()
        self.load_statistics()
    
    def init_ui(self):
        self.setWindowTitle('📊 Панель управления')
        self.setMinimumSize(1000, 600)
        
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Заголовок
        title_label = QLabel('📊 Статистика общежития')
        title_label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #2c3e50;
                padding: 10px;
            }
        """)
        layout.addWidget(title_label)
        
        # Сетка для карточек статистики
        grid = QGridLayout()
        grid.setSpacing(15)
        
        # Создание карточек
        self.stats_cards = {}
        stats_keys = [
            ('total_students', '👥 Всего студентов', '#3498db'),
            ('total_rooms', '🚪 Всего комнат', '#27ae60'),
            ('total_buildings', '🏢 Всего корпусов', '#e74c3c'),
            ('occupied_rooms', '🛏️ Занятых комнат', '#f39c12'),
            ('active_checkins', '✅ Активных заселений', '#9b59b6'),
            ('occupancy_rate', '📈 Процент заселенности', '#1abc9c'),
        ]
        
        row = 0
        col = 0
        for key, title, color in stats_keys:
            card = self.create_stat_card(title, '0', color)
            self.stats_cards[key] = card
            grid.addWidget(card, row, col)
            col += 1
            if col > 2:
                col = 0
                row += 1
        
        layout.addLayout(grid)
        
        # Распределение по полу
        gender_frame = QFrame()
        gender_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 8px;
                padding: 15px;
                border: 2px solid #ecf0f1;
            }
        """)
        gender_layout = QVBoxLayout()
        gender_title = QLabel('👥 Распределение по полу')
        gender_title.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #2c3e50;
                margin-bottom: 10px;
            }
        """)
        self.gender_label = QLabel('Мужчин: 0 | Женщин: 0 | Всего: 0')
        self.gender_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #34495e;
                padding: 10px;
            }
        """)
        gender_layout.addWidget(gender_title)
        gender_layout.addWidget(self.gender_label)
        gender_frame.setLayout(gender_layout)
        
        layout.addWidget(gender_frame)
        layout.addStretch()
        
        # Кнопка обновления
        refresh_btn = QPushButton('🔄 Обновить статистику')
        refresh_btn.setProperty("class", "action")
        refresh_btn.clicked.connect(self.load_statistics)
        layout.addWidget(refresh_btn)
        
        self.setLayout(layout)
    
    def create_stat_card(self, title, value, color):
        """Создание карточки статистики"""
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {color}, stop:1 #ffffff);
                border-radius: 10px;
                padding: 20px;
                border: 2px solid {color};
            }}
        """)
        
        layout = QVBoxLayout()
        
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: 600;
                color: #2c3e50;
                margin-bottom: 5px;
            }
        """)
        
        value_label = QLabel(value)
        value_label.setObjectName("value")
        value_label.setStyleSheet("""
            QLabel#value {
                font-size: 32px;
                font-weight: bold;
                color: #2c3e50;
            }
        """)
        
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        frame.setLayout(layout)
        
        return frame
    
    def load_statistics(self):
        """Загрузка статистики"""
        try:
            stats = self.statistics.get_all_statistics()
            
            # Обновление карточек
            if 'total_students' in self.stats_cards:
                self.update_card_value(self.stats_cards['total_students'], str(stats.get('total_students', 0)))
            if 'total_rooms' in self.stats_cards:
                self.update_card_value(self.stats_cards['total_rooms'], str(stats.get('total_rooms', 0)))
            if 'total_buildings' in self.stats_cards:
                self.update_card_value(self.stats_cards['total_buildings'], str(stats.get('total_buildings', 0)))
            if 'occupied_rooms' in self.stats_cards:
                self.update_card_value(self.stats_cards['occupied_rooms'], str(stats.get('occupied_rooms', 0)))
            if 'active_checkins' in self.stats_cards:
                self.update_card_value(self.stats_cards['active_checkins'], str(stats.get('active_checkins', 0)))
            if 'occupancy_rate' in self.stats_cards:
                rate = stats.get('occupancy_rate', 0)
                self.update_card_value(self.stats_cards['occupancy_rate'], f"{rate}%")
            
            # Распределение по полу
            gender = stats.get('gender_distribution', {})
            self.gender_label.setText(
                f"👨 Мужчин: {gender.get('М', 0)} | "
                f"👩 Женщин: {gender.get('Ж', 0)} | "
                f"👥 Всего: {gender.get('Всего', 0)}"
            )
            
            logger.info("Статистика обновлена")
        except Exception as e:
            logger.error(f"Ошибка загрузки статистики: {e}")
    
    def update_card_value(self, card, value):
        """Обновление значения в карточке"""
        layout = card.layout()
        if layout and layout.count() > 1:
            value_label = layout.itemAt(1).widget()
            if value_label:
                value_label.setText(value)

