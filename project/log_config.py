import logging
import colorlog
from logging.handlers import RotatingFileHandler
import sys



def setup_logging():
    logger = logging.getLogger() # возвращает корневой логгер (управляет общими настройками)
    logger.setLevel(logging.DEBUG)  # обрабатывать все уровни

    # форматтер для консоли (какие поля показывать, в каком порядке)
    console_formatter = colorlog.ColoredFormatter(
        '%(log_color)s%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S',
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        }
    )

    console_handler = logging.StreamHandler(sys.stdout) # вывод соо в консоль
    console_handler.setLevel(logging.DEBUG) # показывает соо всех уровней
    console_handler.setFormatter(console_formatter) # делает соо цветными

    # форматтер для файла
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
    )

    # файловый обработчик
    file_handler = RotatingFileHandler('app.log', maxBytes=5_000_000, backupCount=3, encoding='utf-8') # создает файл, хранить три файла
    file_handler.setLevel(logging.WARNING)   # В файл записываются только предупреждения и выше
    file_handler.setFormatter(file_formatter)

    # добавляем обработчики в корневой логгер
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

# вызываем при старте приложения
logger = setup_logging()