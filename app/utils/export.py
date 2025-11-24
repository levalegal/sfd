"""
Модуль экспорта данных
"""
import csv
from pathlib import Path
from datetime import datetime
from app.utils.logger import setup_logger

logger = setup_logger('export')


def export_students_to_csv(students, filename=None):
    """Экспорт студентов в CSV"""
    if filename is None:
        filename = f"students_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['ID', 'Фамилия', 'Имя', 'Отчество', 'Пол', 'Телефон', 'Email', 'Группа'])
            for student in students:
                writer.writerow(student)
        logger.info(f"Экспортировано {len(students)} студентов в {filename}")
        return filename
    except Exception as e:
        logger.error(f"Ошибка экспорта: {e}")
        raise


def export_checkins_to_csv(checkins, filename=None):
    """Экспорт заселений в CSV"""
    if filename is None:
        filename = f"checkins_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['ID', 'Студент', 'Комендант', 'Корпус', 'Адрес', 'Этаж', 'Комната', 'Дата заселения'])
            for checkin in checkins:
                writer.writerow([
                    checkin[0], checkin[5], checkin[6], checkin[9], 
                    checkin[10], checkin[8], checkin[7], checkin[4]
                ])
        logger.info(f"Экспортировано {len(checkins)} заселений в {filename}")
        return filename
    except Exception as e:
        logger.error(f"Ошибка экспорта: {e}")
        raise

