

import sys
import time
import json
import socket
import argparse
import log.client_log_config
import logging
import threading
from get_send import get_msg_from_client,send_coding_msg_to_client
from decor import log

LOG = logging.getLogger('clients')
@log
def exit_message(account_name):
    """Функция создаёт словарь с сообщением о выходе"""
    return {
        "action": "exit",
         "account_name": account_name
    }

@log
def message_from_server(another_sock, my_username):
    """Функция - обработчик сообщений других пользователей, поступающих с сервера"""
    while True:
        try:
            data = get_msg_from_client(another_sock)
            if "action" in data and data["action"] == "message" and \
                    "sender" in data and "destination" in data \
                    and "message_text" in data and data["destination"] == my_username:
                print(f'\nПолучено сообщение от пользователя {data["sender"]}:'
                      f'\n{data["message_text"]}')
                LOG.info(f'Получено сообщение от пользователя {data["sender"]}:'
                            f'\n{data["message_text"]}')
            else:
                LOG.error(f'Получено некорректное сообщение с сервера: {data}')
       
        except:
            LOG.critical(f'Потеряно соединение с сервером.')
            break  

 
@log
def create_message_to_another_client(client_sock,account_name='Guest'):
    """Функция запрашивает текст сообщения и возвращает его.
    Так же завершает работу при вводе подобной комманды
    """
    to_user = input('Введите получателя сообщения: ')
    message = input('Введите сообщение для отправки: ')
    message_dict = {
        "action": "message",
        "sender": account_name,
        "destination": to_user,
        "message_text": message
    }
    LOG.debug(f'Сформирован словарь сообщения: {message_dict}')
    try:
        send_coding_msg_to_client(client_sock, message_dict)
        LOG.info(f'Отправлено сообщение для пользователя {to_user}')
    except:
        LOG.critical('Потеряно соединение с сервером.')
        sys.exit(1)

@log
def user_interactive(sock, username):
    """Функция взаимодействия с пользователем, запрашивает команды, отправляет сообщения"""
  
    while True:
        command = input('Введите команду: ')
        if command == 'message':
            create_message_to_another_client(sock, username)
        
        elif command == 'exit':
            send_coding_msg_to_client(sock, exit_message(username))
            print('Завершение соединения.')
            LOG.info('Завершение работы по команде пользователя.')
            # Задержка неоходима, чтобы успело уйти сообщение о выходе
            time.sleep(0.5)
            break
        else:
            print('Команда не распознана, попробойте снова.')

@log
def create_presence(account_name):
    """Функция генерирует запрос о присутствии клиента"""
    out = {
        "action": "presence",
        "user": {
            "account_name": account_name
        }
    }
    LOG.debug(f'Сформировано сообщение для пользователя {account_name}')
    return out

@log
def process_response_ans(message):
   
    LOG.debug(f'Разбор приветственного сообщения от сервера: {message}')
    if "response" in message:
        if message["response"] == 200:
            return '200 : OK'
        elif message["response"] == 400:
            LOG.info(f"Oшибка регистрации")

    


@log
def arg_parser():
    """Создаём парсер аргументов коммандной строки
    и читаем параметры, возвращаем 3 параметра
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default="127.0.0.1", nargs='?')
    parser.add_argument('port', default=7777, type=int, nargs='?')
    parser.add_argument('-n', '--name', default=None, nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    server_host = namespace.addr
    server_port = namespace.port
    client_name = namespace.name
        # проверим подходящий номер порта
    if not 1023 < server_port < 65536:
        LOG.critical(
            f'Попытка запуска клиента с неподходящим номером порта: {server_port}. '
            f'Допустимы адреса с 1024 до 65535. Клиент завершается.')
        sys.exit(1)
    


    return server_host, server_port,client_name

def main():
    print('Чат. Клиентский модуль.')
    """Загружаем параметы коммандной строки"""
    server_host, server_port,client_name = arg_parser()

    LOG.info(
        f'Запущен клиент с парамертами: адрес сервера: {server_host}, '
        f'порт: {server_port}')
    
   
    
    
    # Если имя пользователя не было задано, необходимо запросить пользователя.
    if not client_name:
        client_name = input('Введите имя пользователя: ')

    LOG.info(
        f'Запущен клиент с парамертами: адрес сервера: {server_host}, '
        f'порт: {server_port}, имя пользователя: {client_name}')
    print("далее сокет")
    # Инициализация сокета и сообщение серверу о нашем появлении
    try:
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.connect((server_host, server_port))
        send_coding_msg_to_client(transport, create_presence(client_name))
        print("отправлено")
        answer = process_response_ans(get_msg_from_client(transport))
        print(f'Установлено соединение с сервером. Ответ сервера: {answer}')
        print(f'Установлено соединение с сервером.')
  
    except (ConnectionRefusedError, ConnectionError):
        LOG.critical(
            f'Не удалось подключиться к серверу {server_host}:{server_port}, '
            f'конечный компьютер отверг запрос на подключение.')
        sys.exit(1)
    else:
        # Если соединение с сервером установлено корректно,
        # запускаем клиенский процесс приёма сообщний
        receiver = threading.Thread(target=message_from_server, args=(transport, client_name))
        receiver.daemon = True
        receiver.start()

        # затем запускаем отправку сообщений и взаимодействие с пользователем.
        user_interface = threading.Thread(target=user_interactive, args=(transport, client_name))
        user_interface.daemon = True
        user_interface.start()
        LOG.debug('Запущены процессы')

        # Watchdog основной цикл, если один из потоков завершён,
        # то значит или потеряно соединение или пользователь
        # ввёл exit. Поскольку все события обработываются в потоках,
        # достаточно просто завершить цикл.
        while True:
            time.sleep(1)
            if receiver.is_alive() and user_interface.is_alive():
                continue
            break


if __name__ == '__main__':
    main()







