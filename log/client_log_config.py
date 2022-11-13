import sys
import os
import logging
#  создаем   объект логера
LOG_CLIENT = logging.getLogger("client")

# создаём формировщик логов:
format_msg = logging.Formatter('%(asctime)s %(levelname)s %(filename)s %(message)s')

# файл для вывода логов куда пишем логи
# переменная путь до файла записи и кодировка
clientlog_file = logging.FileHandler('clients.log',encoding='utf8')
# метод для переменной пути файла формат записи лога
clientlog_file.setFormatter(format_msg)

#создаем требования для потока вывода логов откуда пишем логи
# логи берем из потока ошибок
hand_log = logging.StreamHandler(sys.stderr)
# устанавливаем уровень важности сообщения от warning  и выше
hand_log.setLevel(logging.WARNING)
# устанавливаем формат записи сообщения из потока ошибок
hand_log.setFormatter(format_msg)


# СВОЙ регистратор логов работаем с объектом логирования применяем ранее созданные 
# настройки
#-------------------------
# у объекта логгера вызываем метод для для добавления  переменной с инф по забору логов
LOG_CLIENT.addHandler(hand_log)
# у объекта логгера вызываем метод для для добавления  переменной с инф куда записывать логи
LOG_CLIENT.addHandler(clientlog_file)
# у объекта логгера вызываем метод для установления важности сообщений будет записывать debug и выше
LOG_CLIENT.setLevel(logging.DEBUG)

# отладка
if __name__ == '__main__':
    LOG_CLIENT.critical('Критическая ошибка')
    LOG_CLIENT.error('Ошибка')
    LOG_CLIENT.debug('Отладочная информация')
    LOG_CLIENT.info('Информационное сообщение')