import unittest,client,time
class TestClient(unittest.TestCase):
    def testpresence(self,user="newuser"):
        self.user = user
        test_client = client.presence(self.user)
        test_client[time]=99
        self.assertEqual(client.presence(self.user), {
        "action": "presence",
        "time": 99,
        "user": {"account_name": self.user}
    })


    def testanswerfromserver(self):
        host = "127.0.0.1"
        port = 7777
        test_answer = client.get_msgfromserver(client.push_coding_msg(host,port))
        if test_answer["response"] == 200: 
            self.assertEqual(test_answer["response"] == 200,'200 : OK')
        if test_answer["response"] == 400: 
            self.assertEqual(test_answer["response"] == 400,'400 : Bad Request')

    def testpush_coding_msg(self,host="127.0.0.1",port=7777):
        self.host = host
        self.port = port
        self.assertEqual(client.push_coding_msg(self.host,self.port),"<socket.socket fd=3, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('127.0.0.1', 38280), raddr=('127.0.0.1', 7777)>","ГУД ТЕСТ ПРОШЕЛ")
    
    def get_msgfromserver(self,host="127.0.0.1",port=7777):
        self.host = host
        self.port = port
        test_msg = client.push_coding_msg(self.host,self.port)
        if test_msg["response"] == 200: 
            self.assertEqual(test_msg["response"] == 200,'200 : OK')
        if test_msg["response"] == 400: 
            self.assertEqual(test_msg["response"] == 400,'400 : Bad Request')

if __name__ == '__main__':
    unittest.main()