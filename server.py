import sys
import json
import select
import socket
import logging
from get_send import get_msg_from_client,send_coding_msg_to_client
import log.server_log_config
from decor import log
LOG = logging.getLogger('server')

# парсим и валидируем сообщение от клиента на наличие \
# создания соединения или на получения сообщения от клиента, формируем ответ 
@log
def message_from_client(data,data_list,client_socket,clients,to_senders:dict):
    if "action" in data and data["action"] == "presence":
        if data['user']['account_name'] not in to_senders.keys():
            to_senders[data['user']['account_name']] = client_socket
            send_coding_msg_to_client(client_socket, {"response": 200})
        else:
            response = {"response": 400}
            send_coding_msg_to_client(client_socket, response)
            clients.remove(client_socket)
            client_socket.close()
        return
    elif "action" in data and data["action"] == "message" and \
            "destination" in data\
            and "sender" in data and "message_text" in data:
        data_list.append(data)
        return
    # Если клиент выходит
    elif "action" in data and data["action"] == "exit" and "action" in data:
        data_list.remove(to_senders[data["action"]])
        to_senders[data["action"]].close()
        del to_senders[data["action"]]
        return
    # Иначе отдаём Bad request
    else:
        response = {"response": 400}
        send_coding_msg_to_client(client_socket, response)
        return
        
@log
def message_to_target_client(data, to_senders, sends):
    
    if data["destination"] in to_senders and to_senders[data["destination"]] in sends:
        send_coding_msg_to_client(to_senders[data["destination"]], data)
        LOG.info(f'Отправлено сообщение пользователю {data["destination"]} '
                    f'от пользователя {data["sender"]}.')
    elif data["destination"] in to_senders and to_senders[data["destination"]] not in sends:
        raise (f"Соединение разорвано")
    else:
        LOG.error(
            f'Пользователь {data["destination"]} не зарегистрирован на сервере, '
            f'отправка сообщения невозможна.')

    

def main():
    try:
        if '-p' in sys.argv:
            listen_port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            listen_port = 7777
        if listen_port < 1024 or listen_port > 65535:
            raise ValueError
    except IndexError:
        print('нужен порт.')
        sys.exit(1)
    except ValueError:
        print(
            'не правильный диапазон')
        sys.exit(1)

    

    try:
        if '-a' in sys.argv:
            listen_address = sys.argv[sys.argv.index('-a') + 1]
        else:
            listen_address = ''

    except IndexError:
        LOG.critical(
            f'Попытка запуска сервера с указанием неподходящего порта '
            f'{listen_port}. Допустимы адреса с 1024 до 65535.')
        print(
            'указать адрес сервера.')
        sys.exit(1)

    # сокет сессии

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.bind((listen_address, listen_port))
    transport.settimeout(0.5)
    LOG.info(f'Подготовлен транспортный сокет{transport}  адрес {listen_address} порт {listen_port}')
     # список клиентов , очередь сообщений
    clients = []
    data_list = []
     # Словарь, содержащий имена пользователей и соответствующие им сокеты.
    to_senders = dict()
    # Слушаем порт
    transport.listen(5)
 
   
    

    
    
    print('\nОжидание подключения...')
    
    while True:
        # Ждём подключения, если таймаут вышел, ловим исключение.
        try:
            client_sockets, client_address = transport.accept()
        except OSError:
            pass
        else:
            LOG.info(f'Установлено соедение с ПК {client_address}')
            clients.append(client_sockets)
            print(clients)

        reads = []
        sends = []
        err_lst = []
        # Проверяем на наличие ждущих клиентов
        try:
            if clients:
                reads, sends, err_lst = select.select(clients, clients, [], 0)
        except OSError:
            pass

        # принимаем сообщения и если ошибка, исключаем клиента.
        print(reads)
        if reads:
            print(f'{reads}+второй')
            
            for client_sockets_with_message in reads:
                try:
                    message_from_client(get_msg_from_client(client_sockets_with_message),
                                           data_list, client_sockets_with_message, clients, to_senders)
                except Exception:
                    LOG.info(f'Клиент {client_sockets_with_message.getpeername()} '
                                f'отключился от сервера.')
                    clients.remove(client_sockets_with_message)

        # Если есть сообщения, обрабатываем каждое.
        for msg in data_list:
            try:
                message_to_target_client(msg, to_senders, sends)
            except Exception:
                LOG.info(f'Связь с клиентом с именем {msg["destination"]} была потеряна')
                clients.remove(to_senders[msg["destination"]])
                del to_senders[msg["destination"]]
        data_list.clear()


if __name__ == '__main__':
    main()








