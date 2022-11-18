import sys
import json
import socket
import logging
import log.server_log_config
from decor import log

LOG = logging.getLogger('server')
# получаем сообщение от клиента и декодируем, формируем из json словарь  
@log  
def get_msgfromclient(tr_socket):
    encoded_resp = tr_socket.recv(1024)
    if isinstance(encoded_resp, bytes):
        json_resp = encoded_resp.decode("utf-8")
        resp = json.loads(json_resp)
        if isinstance(resp, dict):
            print(resp)
            return resp
        raise ValueError
    raise ValueError

# парсим и валидируем сообщение от клиента, формируем ответ 
@log
def answer_from_client(answerclient:dict):
    
    if "action" in answerclient and answerclient["action"] == "presence" \
            and "user" in answerclient and answerclient["user"]["account_name"] == 'newuser':
        print("response: 200")
        return {"response": 200}
    print("response: 400")
    return {
        "response": 400,
        "error": 'Bad Request'
    }
#  кодируем и отправляем ответ клиенту 
@log
def push_coding_msg_toclient(tr_socket,msgtoclient):
    js_msg = json.dumps(msgtoclient)
    encoded_msg = js_msg.encode("utf-8")
    tr_socket.send(encoded_msg)
    print(encoded_msg)
   
  

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
        print(
            'указать адрес сервера.')
        sys.exit(1)

    # сокет сессии

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.bind((listen_address, listen_port))

    # Слушаем порт

    transport.listen(5)

    while True:
        # сессия клиента
        tr_socket, client_address = transport.accept()
        message_from_cient = get_msgfromclient(tr_socket)
        # print(message_from_cient)
           
        response = answer_from_client(message_from_cient)
        print(response)
        push_coding_msg_toclient(tr_socket, response)
        print(f"Сообщение:  было отправлено клиентом: {client_address}")
        tr_socket.close()
       


if __name__ == '__main__':
    main()








