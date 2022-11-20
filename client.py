import sys
import json
import socket
import log.client_log_config
import logging
from decor import log

LOG = logging.getLogger('client')
# формируем словарь dict  с атрибутами для нового пользователя
@log
def presence(newuser):
    output = {
        "action": "presence",
        # "time": time.time(),
        "user": {"account_name": newuser}
    }
    return output
   
# формируем клиента и кодируем сообщение отправляем на сервер
@log
def push_coding_msg(host,port):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((host,port))
    pushmsg = presence("newuser")
    json_pushmsg = json.dumps(pushmsg)
    encoded_msg = json_pushmsg.encode("utf-8")
    s.send(encoded_msg)
    # s.close()
    print("сообщение отправлено")
    print(s)
    return s
# получаем сообщение с сервера и декодируем, формируем из json объекта словарь 
@log   
def get_msgfromserver(socketsession):
    
    encoded_resp = socketsession.recv(1024)
    if isinstance(encoded_resp, bytes):
        json_resp = encoded_resp.decode("utf-8")
        resp = json.loads(json_resp)
        if isinstance(resp, dict):
            print(resp,f"сообщение получено")
            return resp
        raise ValueError
    raise ValueError

# парсим словарь
@log
def answerfromserver():
    answer = get_msgfromserver()
    if "response" in answer:
        if answer["response"] == 200:
            print(f"200 : OK")
            return '200 : OK'
        return f'400 : {answer["error"]}'
    raise ValueError

def main():
    
    # создаем параметры командной строки
    try:
        server_host =  sys.argv[1]
        server_port = int(sys.argv[2])
        if server_port < 1024 or server_port > 65535:
            raise ValueError
    except IndexError:
        server_host = "127.0.0.1"
        server_port = 7777
    except ValueError:
        print('порт не верный')
        sys.exit(1)

    # вызываем фукцию для клиента открытия сокета создания сообщения и кодировки
    S = push_coding_msg(server_host,server_port)
    get_msgfromserver(S)
    
   


if __name__ == '__main__':
    main()







