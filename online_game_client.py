import socket

from enums import Player_Commands


class Online_Game_Client:
    SERVER_PORT = 3333
    SERVER_IP = '192.168.68.136'

    def __init__(self) -> None:
        self.my_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.my_sock.connect((self.SERVER_IP, self.SERVER_PORT))
        print('client connected')

    def mainloop(self):
        while True:
            self.my_sock.send(input('enter something:  ').encode())


def main():
    client = Online_Game_Client()
    client.mainloop()


if __name__ == "__main__":
    main()
