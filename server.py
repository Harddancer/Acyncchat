import sys
import json
import select
import socket
import logging
from tkinter import S
import log.server_log_config
from decor import log

LOG = logging.getLogger('server')
# получаем сообщение от клиента и декодируем, формируем из json словарь  
@log 
def get_msg_from_client_registraton(sockets,names):
    responses = sockets.recv(1024).decode("utf-8")
    encoded_resp = json.loads(responses)
    if isinstance(encoded_resp, dict):
        print(f"Новый пользователь {encoded_resp['user']['account_name']}")
        if encoded_resp['user']['account_name'] not in names.keys():
            names[sockets] = encoded_resp['user']['account_name']
            
        return encoded_resp,
    raise ValueError

@log
def push_coding_msg_to_client_registration(sockets,msg_from_client):
    if "action" in msg_from_client and msg_from_client["action"] == "presence" \
        and "user" in msg_from_client and msg_from_client["user"]["account_name"] != "":
        msg ={"response":200,"Client":msg_from_client['user']['account_name']}
        js_msg = json.dumps(msg)
        encoded_msg = js_msg.encode("utf-8")
        sockets.send(encoded_msg)
        print(str(encoded_msg))
    else:
        msg ={"response":400,"Отказ в регистрации Клиент":msg_from_client['user']['account_name']}
        js_msg = json.dumps(msg)
        encoded_msg = js_msg.encode("utf-8")
        sockets.send(encoded_msg)
        print(encoded_msg)


# парсим и валидируем сообщение от клиента на наличие \
# создания соединения или на получения сообщения от клиента, формируем ответ 
@log
def message_from_client(data):
    responses = data.decode("utf-8")
    answerclient = json.loads(responses)
    if "action" in answerclient and answerclient["action"] == "message" \
        and answerclient["message_text"] != "":
        
        print("сообщение получено")
        return answerclient,answerclient["destination"]
    else:
        print("Не корректное соообщение")

@log
def message_to_all_encode(data:dict):
    new_msg ={
        "action":"message",
        "sender":data['account_name'],
        "message_text":data['message_text']

    }
    js_answerclient = json.dumps(new_msg)
    msg_to_clients = js_answerclient.encode("utf-8")
    return msg_to_clients
    

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
    #transport.settimeout(100)
    LOG.info(f'Подготовлен транспортный сокет{transport}  адрес {listen_address} порт {listen_port}')
    
    # Слушаем порт

    transport.listen(5)
 
   
    #список клиентов , очередь сообщений
    all_clients_reg = [transport]
    
    messages = {}
    names = dict()
    
    
    print('\nОжидание подключения...')
    
    while True:
        try:
            reads, send, excepts = select.select(all_clients_reg, all_clients_reg, all_clients_reg)
        except OSError:
            pass
        else:
            LOG.info(f'Cокеты подготовлены {reads}')
            print(reads)
            
        #Проверяем на наличие ждущих клиентов(сокетов) клиенты кот устанавливают соединение
        if reads:
            
            for s in reads:
                if s == transport:
                    conn,client_addr = s.accept()
                    print("Connected by", client_addr)
                    msg_from_client = get_msg_from_client_registraton(conn,names)
                    push_coding_msg_to_client_registration(conn,msg_from_client)
                    conn.setblocking(0)
                    all_clients_reg.append(conn)
                else:
                    #print("если это НЕ серверный сокет")
                    data = s.recv(1024)
                    if data:
                        messages.get(s, None)
                        messages[s]=data
                        msg,to_client= message_from_client(data)
                        for sockets in send:
                            if sockets  in names.keys():
                                to_clients = names[sockets]
                                if to_client == to_clients:
                                    sockets.send(message_to_all_encode(msg,to_clients))
                                    print(f"отправлено {to_client}")
                    if not data:
                        print("сообщения не было нечего отправлять")
                    else:
                        print('Клиент отключился...')
                        # если сообщений нет, то клиент
                        # закрыл соединение или отвалился 
                        # удаляем его сокет из всех очередей
                    
                        all_clients_reg.remove(s)
                        
                                # закрываем сокет как положено, тем 
                                # самым очищаем используемые ресурсы
                        s.close()
                                # удаляем сообщения для данного сокета
                        del messages[s]

      

     

        
if __name__ == '__main__':
    main()








