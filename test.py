import unittest
import time
import socket
import urllib.request
from http import HTTPStatus
from app.hello import setup_server, get_respose, kill_server


class TestServer(unittest.TestCase):
    port = '8088'
    local_ip = '0.0.0.0'
    local_host_ip = socket.gethostbyname(socket.gethostname())
    local_ip_url = 'http://' + local_ip + ':' + port
    local_host_ip_url = 'http://' + local_host_ip + ':' + port

    def test_setup_server(self):
        """
        test setup server on custom port
        """
        setup_server(self.port)
        # server wont be available very immediately
        time.sleep(3)
        with urllib.request.urlopen(self.local_ip_url) as response:
            assert response.code == HTTPStatus.OK

        with urllib.request.urlopen(self.local_host_ip_url) as response:
            assert response.code == HTTPStatus.OK

    def test_server_response(self):
        """
        test get server response
        """
        code, response = get_respose(self.local_ip_url)
        assert code == HTTPStatus.OK
        assert response == b'Hi there, !'

    def test_server_response_with_param(self):
        """
        test get server response with param
        """
        code, response = get_respose(self.local_ip_url+ '/test')
        assert code == HTTPStatus.OK
        assert response == b'Hi there, test!'


if __name__ == '__main__':
    unittest.main()
