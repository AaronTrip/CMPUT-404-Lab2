#!/usr/bin/env python3


from multiprocessing.context import Process
from multi_proxy_client import BUFFER_SIZE, HOST, PORT
import socket
import time
from multiprocessing import process

HOST = ''
PORT = 8001
BUFFER_SIZE = 1024


def main():

    #create socket, bind, listen
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        #allow reused address
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(1)

        while True:

            # accept connections and start a process daemon for handling multiple connections
            conn, addr = s.accept()
            p = Process(target=handle_echo, args=(addr, conn))
            p.daemon = True
            p.start()
            print("Started process ", p)


def handle_echo(addr, conn):
    print("Connected by ", addr)

    full_data = conn.recv(BUFFER_SIZE)
    conn.sendall(full_data)
    conn.shutdown(socket.SHUT_RDWR)
    conn.close()


if __name__ == "__main__":
    main()
