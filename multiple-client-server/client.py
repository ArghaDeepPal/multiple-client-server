import socket

from numpy import double, mask_indices

IP = socket.gethostbyname(socket.gethostname())
PORT = 9000
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    print(f"[CONNECTED] Client connected to server at {IP}:{PORT}")

    connected = True
    while connected:
        print("1.Send a Message\n2.Get the time\n3.Wikipedia Search\n4.How Long have I been connected?\n5.Exit")
        msg = input("> ")
        if msg=="1":
            msg=input("Write your message: ")
            client.send(msg.encode(FORMAT))
            msg = client.recv(SIZE).decode(FORMAT)
            if msg!="!noresponse":
             print(f"[SERVER] {msg}")
        elif msg=="2":
            client.send(msg.encode(FORMAT))
            msg = client.recv(SIZE).decode(FORMAT)
            print(f"[SERVER] {msg}")
        elif msg=="3":
            msg="!wiki "+input("Write your wiki query: ")
            client.send(msg.encode(FORMAT))
            msg = client.recv(SIZE).decode(FORMAT)
            print(f"[SERVER] {msg}")
        elif msg=="4":
            client.send(msg.encode(FORMAT))
            msg = client.recv(SIZE).decode(FORMAT)
            time=double(msg)
            if time>60:
                mins=0
                while time>60:
                    time=time-60
                    mins=mins+1
                print(f"[SERVER] {mins} mins {time} secs")
            else:
                print(f"[SERVER] {msg} secs")
        elif msg == "5":
            msg="!DISCONNECT"
            client.send(msg.encode(FORMAT))
            connected = False
        else:
            print("Option does not exist")
            

if __name__ == "__main__":
    main()
