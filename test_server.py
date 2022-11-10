import unittest,server,socket
class TestServer(unittest.TestCase):
    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.bind(("127.0.0.1", 7777))
    tr_socket, client_address = transport.accept()
    
    def testanswer_from_client(self):
        host = "127.0.0.1"
        port = 7777
        test_answer = server.get_msgfromclient(server.push_coding_msg(host,port))
        if test_answer["response"] == 200: 
            self.assertEqual(test_answer["response"] == 200,'200 : OK')
        if test_answer["response"] == 400: 
            self.assertEqual(test_answer["response"] == 400,'400 : Bad Request')

    def testpush_coding_msg_toclient(self,tr_socket,msg={"response": 200}):
        self.tr_socket = tr_socket
        self.msg = msg
        
        self.assertEqual(server.push_coding_msg(self.tr_socket,self.msg),"<socket.socket fd=3, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('127.0.0.1', 38280), raddr=('127.0.0.1', 7777)>","ГУД ТЕСТ ПРОШЕЛ")
    
    def testget_msgfromclient(self,tr_socket):
       self.tr_socket = tr_socket
       test_msg = server.push_coding_msg_toclient(self,tr_socket,msg={"response": 200})
       if test_msg["response"] == 200: 
            self.assertEqual(test_msg["response"] == 200,'200 : OK')
        
