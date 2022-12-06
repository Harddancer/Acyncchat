

import sys
import json
import socket
import argparse
import log.client_log_config
import logging
from decor import log

LOG = logging.getLogger('client')
# формируем словарь dict  с атрибутами для нового пользователя
NAME = ""
@log
def reristration_user():
    nikname = input("Ваше имя")
    output = {
        "action": "presence",
        "user": {"account_name": nikname}
    }
    LOG.debug(f'Регистрация пользователя {output["user"]["account_name"]}')
    global NAME 
    NAME = output["user"]["account_name"]
    return output


# формируем клиента и кодируем сообщение отправляем на сервер
@log
def push_coding_msg_registration(socket,reg_msg):
    json_pushmsg = json.dumps(reg_msg)
    encoded_msg = json_pushmsg.encode("utf-8")
    socket.send(encoded_msg)
    print("сообщение на регистрацию отправлено")
    return encoded_msg

# получаем сообщение с сервера и декодируем, формируем из json объекта словарь 
@log   
def get_msg_registration(socket):
    encoded_resp = socket.recv(1024)
    if isinstance(encoded_resp, bytes):
        response_server = json.loads(encoded_resp.decode("utf-8"))
        if isinstance(response_server, dict):
            if "response" in response_server and response_server["response"] == 200:
                print(response_server['Client'],f"\nДобро пожаловать в чат!")
                return '200 : OK'
            else:
                print(f'Клиент не указал имя в регистрации отказано')
                sys.exit(1)
        
    raise ValueError

# клдируем сообщение для  клиентов
@log
def push_coding_msg_to_clients(socket,cli_msg):
    """
    # кодируем сообщение для  клиентов
    """
    json_pushmsg = json.dumps(cli_msg)
    encoded_msg = json_pushmsg.encode("utf-8")
    socket.send(encoded_msg)
    print("сообщение для клиентов отправленно")
    return encoded_msg


   
@log
def get_message_from_another_clients(client_socket):
    """Функция - обработчик сообщений других пользователей, поступающих с сервера"""
    encoded_resp = client_socket.recv(1024)
    if isinstance(encoded_resp, bytes):
        response_server = json.loads(encoded_resp.decode("utf-8"))
        if isinstance(response_server, dict) and "action" in response_server and response_server["action"] == "message" and \
            "sender" in response_server and "message_text" in response_server:
            print(f'Получено сообщение от пользователя '
              f'{response_server["sender"]}:\n{response_server["message_text"]}')
            LOG.info(f'Получено сообщение от пользователя '
                    f'{response_server["sender"]}:\n{response_server["message_text"]}')
    else:
        LOG.error(f'Получено некорректное сообщение с сервера: {response_server}')

@log
def create_message_to_another_client(client_sock):
    """Функция запрашивает текст сообщения и возвращает его.
    Так же завершает работу при вводе подобной комманды
    """
    message = input('Введите сообщение для отправки или \'exit\' для завершения работы: ')
    if message == 'exit':
        client_sock.close()
        LOG.info('Завершение работы по команде пользователя.')
        print('Спасибо за использование чата!')
        sys.exit(1)
    else:
        message_dict = {
        "action": "message",
        "account_name": NAME,
        "message_text": message
        }
        LOG.debug(f'Сформирован словарь сообщения: {message_dict}')
        return message_dict

@log
def arg_parser():
    """Создаём парсер аргументов коммандной строки
    и читаем параметры, возвращаем 3 параметра
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default="127.0.0.1", nargs='?')
    parser.add_argument('port', default=7777, type=int, nargs='?')
    parser.add_argument('-m', '--mode', default='listen', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    server_host = namespace.addr
    server_port = namespace.port
    client_mode = namespace.mode
        # проверим подходящий номер порта
    if not 1023 < server_port < 65536:
        LOG.critical(
            f'Попытка запуска клиента с неподходящим номером порта: {server_port}. '
            f'Допустимы адреса с 1024 до 65535. Клиент завершается.')
        sys.exit(1)
    

    # Проверим допустим ли выбранный режим работы клиента
    if client_mode not in ('listen', 'send'):
        LOG.critical(f'Указан недопустимый режим работы {client_mode}, '
                        f'допустимые режимы: listen , send')
        sys.exit(1)

    return server_host, server_port, client_mode

def main():
    """Загружаем параметы коммандной строки"""
    server_host, server_port, client_mode = arg_parser()

    LOG.info(
        f'Запущен клиент с парамертами: адрес сервера: {server_host}, '
        f'порт: {server_port}, режим работы: {client_mode}')
    
   
    
    
    # Инициализация сокета и сообщение серверу о нашем появлении
    client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client_socket.connect((server_host,server_port))
    
    try:
        push_coding_msg_registration(client_socket,reristration_user())
        get_msg_registration(client_socket)
       
        LOG.info(f'Установлено соединение с сервером.')
    
    except ConnectionRefusedError:
        LOG.critical(
            f'Не удалось подключиться к серверу {server_host}:{server_port}, '
            f'конечный компьютер отверг запрос на подключение.')
        sys.exit(1)
    except json.JSONDecodeError:
        LOG.critical('Не удалось декодировать полученную Json строку.')
        sys.exit(1)


    # Если соединение с сервером установлено корректно,
    # начинаем обмен с ним, согласно требуемому режиму.
    # основной цикл прогрммы:
    if client_mode == 'send':
        print('Режим работы - отправка сообщений.')
    else:
        print('Режим работы - приём сообщений.')
    while True:
            # режим работы - отправка сообщений
            if client_mode == 'send':
                try:
                    push_coding_msg_to_clients(client_socket, create_message_to_another_client(client_socket))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    LOG.error(f'Соединение с сервером {server_host} было потеряно.')
                    sys.exit(1)

            # Режим работы приём:
            if client_mode == 'listen':
                try:
                    get_message_from_another_clients(client_socket)

                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    LOG.error(f'Соединение с сервером {server_host} было потеряно.')
                    sys.exit(1)
       
if __name__ == '__main__':
    main()







