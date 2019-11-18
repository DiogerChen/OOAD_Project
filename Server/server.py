import socket
import threading

serverName = '10.17.79.87'
serverPort = 5555

class Echo(threading.Thread):
    def __init__(self, conn, address):
        threading.Thread.__init__(self)
        self.conn = conn
        self.address = address

    def run(self):
        while True:
            data = self.conn.recv(2048)
            if data and data != b'quit':
                data=data.upper()
                self.conn.send(data)
                print('{} sent: {}'.format(self.address, data))
            else:
                self.conn.close()
                print('connection closed')
                return

def echo():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('10.17.79.87', 5555))
    sock.listen(10)
    while True:
        conn, address = sock.accept()
        Echo(conn, address).start()


if __name__ == "__main__":
    try:
        echo()
    except KeyboardInterrupt:
        exit()
