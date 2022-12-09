import sys
import json
from decor import log



# получаем сообщение от клиента и декодируем, формируем из json словарь  
@log 
def get_msg_from_client(client_socket):
    responses = client_socket.recv(1024)
    if isinstance(responses, bytes):
        json_response = responses.decode("utf-8")
        encoded_resp = json.loads(json_response)
        if isinstance(encoded_resp, dict):
            return encoded_resp
        else:
            print("Это не словарь")
    else:
        print("Это не байты")
        

@log
def send_coding_msg_to_client(client_socket,msg_from_client):
    if not isinstance(msg_from_client, dict):
        print('Это не словарь2')
    js_message = json.dumps(msg_from_client)
    encoded_message = js_message.encode('utf-8')
    client_socket.send(encoded_message)


      