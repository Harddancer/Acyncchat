import sys
import logging
import log.server_log_config
import log.client_log_config
import traceback
import inspect


if sys.argv[0].find('client') == -1:
 
    LOG = logging.getLogger('server')
else:
 
    LOG = logging.getLogger('client')


# функция
def log(func_to_log):
    "декоратор"
    def log_saver(*args, **kwargs):
        """Обертка"""
        ret = func_to_log(*args, **kwargs)
        LOG.debug(f'Была вызвана функция {func_to_log.__name__} c параметрами {args}, {kwargs}. '
                     f'Вызов из модуля {func_to_log.__module__}. Вызов из'
                     f' функции {traceback.format_stack()[0].strip().split()[-1]}.'
                     f'Вызов из функции {inspect.stack()[1][3]}')
        return ret
    return log_saver


# класс
class Log:
    """Класс-декоратор"""
    def __call__(self, func_to_log):
        def log_saver(*args, **kwargs):
            """Обертка"""
            ret = func_to_log(*args, **kwargs)
            LOG.debug(f'Была вызвана функция {func_to_log.__name__} c параметрами {args}, {kwargs}. '
                         f'Вызов из модуля {func_to_log.__module__}. Вызов из'
                         f' функции {traceback.format_stack()[0].strip().split()[-1]}.'
                         f'Вызов из функции {inspect.stack()[1][1]}')
            return ret
        return log_saver