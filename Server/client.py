import socket
import threading

serverName = '10.17.79.87'
serverPort = 5555

def trans():
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((serverName,serverPort))
    while True:
        sentence = input('Input lowercase sentence:')
        clientSocket.send(sentence.encode())
        modifiedSentence = clientSocket.recv(1024)
        if sentence == 'quit' :
            clientSocket.close()
            print('connection closed')
            break
        print ('From Server:', modifiedSentence.decode())

if __name__ == '__main__':
    trans()


