import logging
import os
from pathlib import Path

# каталог логов
LOG_DIR = "logs"

# Базовый формат для всех логов
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logger(name: str, log_file: str):
    """фабричная функция логгеров"""

    # Создаём папку для логов, если её нет
    Path(LOG_DIR).mkdir(exist_ok=True)

    # Путь к файлу лога
    log_path = os.path.join(LOG_DIR, f"{log_file}.log")

    # Создаем логгер
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Создаем обработчик для записи в файл
    file_handler = logging.FileHandler(log_path, mode="w", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)

    # Создаем форматтер
    formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
    file_handler.setFormatter(formatter)

    # Добавляем обработчик к логгеру
    logger.addHandler(file_handler)

    return logger
