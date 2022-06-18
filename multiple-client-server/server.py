import socket
import threading
import wikipedia
from datetime import datetime
import time
IP = socket.gethostbyname(socket.gethostname())
PORT = 9000
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    starttime=time.perf_counter()
    connected = True
    while connected:
        msg = conn.recv(SIZE).decode(FORMAT)
        if msg == "!DISCONNECT":
            connected = False
            conn.close()
        elif msg=="2":
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            msg = "The time is: " + current_time
            conn.send(msg.encode(FORMAT))
            
        elif msg=="4":
            timenow=time.perf_counter()
            msg=str(timenow-starttime)
            conn.send(msg.encode(FORMAT))
        elif "!wiki" in msg:
            item=msg[6:]
            try:
                search=wikipedia.summary(item,sentences=3)
                msg=search
            except:
                msg="Sorry error getting this wiki search"
            conn.send(msg.encode(FORMAT))

        else :
            print(f"[{addr}] {msg}")
            check=input("Reply?(Y/N)")
            if check=="Y" or check=="y":
                msg=input("Write reply: ")
                conn.send(msg.encode(FORMAT))
            else:
                msg="!noresponse"
                conn.send(msg.encode(FORMAT))

    

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"Server is listening on {IP}:{PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__ == "__main__":
    main()
