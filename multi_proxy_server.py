#!/usr/bin/env python3

from multi_proxy_client import BUFFER_SIZE
import socket, time, sys
from multiprocessing import Process

HOST = ''
PORT = 8001
BUFFER_SIZE = 1024

#get ip
def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        sys.exit()

    print (f'Ip address of {host} is {remote_ip}')
    return remote_ip

def handle_requests(addr, conn):
    print("Connected by ", addr)

    full_data = conn.recv(BUFFER_SIZE)
    conn.sendall(full_data)
    conn.shutdown(socket.SHUT_RDWR)
    conn.close()

def main():

    extern_host = 'www.google.com'
    extern_port = 80


    # create intial socket as proxy start, set it up to listen
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_start:
        #allow reused address
        proxy_start.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        proxy_start.bind((HOST, PORT))
        proxy_start.listen(1)

        while True:

            conn, addr = proxy_start.accept()
            print("connected to ", addr)
            
            # create our other socket that connects to google as proxy end
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_end:
                print("Connecting to google")
                remote_ip = get_remote_ip(extern_host)

                #connect to proxy end
                proxy_end.connect((remote_ip, extern_port))

                # now that we are connected to google with our proxy, allow for multiprocessing
               
                p = Process(target=handle_requests, args=(addr, conn))
                p.daemon = True
                p.start()
                print("Started process ", p)

            conn.close()


if __name__ == "__main__":
    main()







