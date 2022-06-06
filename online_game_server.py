import socket
import threading
import pygame

from enums import Player_Commands


class Online_Game_Server:
    SERVER_PORT = 3333
    SERVER_IP = '192.168.68.136'

    def __init__(self) -> None:
        self.my_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.my_sock.bind((self.SERVER_IP, self.SERVER_PORT))
        print('Server is up and running')

        self._clients = []
        self._client_threads = []

        self._requests = []

        self.get_clients()

    def get_clients(self):
        while True:
            self.my_sock.listen()
            client, client_address = self.my_sock.accept()
            print('Client connected')

            self._clients.append(client)
            self._client_threads.append(
                threading.Thread(target=self.handle_client, args=(client,))
            )

            if len(self._clients) == 1:
                break

    def handle_client(self, client: socket.socket):
        print('handeling client')
        while True:
            message = client.recv(1024).decode()
            print(message)

            self._requests.append(message)
            if message == 'Q':
                break

    def mainloop(self) -> None:
        print('in mainloop')
        for thread in self._client_threads:
            thread.start()
        while True:
            if self._requests:
                print(self._requests)
                self._requests.clear()


def main():
    # server = Online_Game_Server()
    # server.mainloop()
    print(pygame.K_1)


if __name__ == "__main__":
    main()
