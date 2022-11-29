import sys
import os
import logging
import logging.handlers
LOG = logging.getLogger('server')

# создаём формировщик логов
format_msg = logging.Formatter('%(asctime)s %(levelname)s %(filename)s %(message)s')

# Подготовка имени файла для логирования
PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(PATH, 'server.log')

# создаём потоки вывода 
handler_log = logging.StreamHandler(sys.stderr)
handler_log.setFormatter(format_msg)
handler_log.setLevel(logging.ERROR)
LOGS = logging.handlers.TimedRotatingFileHandler(PATH, encoding='utf8', interval=1, when='D')
LOGS.setFormatter(format_msg)

# создаём регистратор и настраиваем его
LOG.addHandler(handler_log)
LOG.addHandler(LOGS)
LOG.setLevel(logging.DEBUG)

# отладка
if __name__ == '__main__':
    LOG.critical('Критическая ошибка')
    LOG.error('Ошибка')
    LOG.debug('Отладочная информация')
    LOG.info('Информационное сообщение')