from concurrent.futures import thread
import pickle
from pydoc import cli
import socket
import threading
import pygame
from dataclasses import dataclass

from enums import Player_Commands


@dataclass
class Player:
    username: str
    ID: int
    sock: socket.socket
    thread: threading.Thread


@dataclass
class Request:
    type: Player_Commands
    player_id: int


class Online_Game_Server:
    SERVER_PORT = 3333
    SERVER_IP = '172.16.17.115'

    def __init__(self) -> None:
        self.my_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.my_sock.bind((self.SERVER_IP, self.SERVER_PORT))
        print('Server is up and running')

        self._players = []
        self._threads = []
        self._requests = []

        self.get_clients()

    def get_clients(self) -> None:
        currentID = 0
        while True:
            self.my_sock.listen()
            client, client_address = self.my_sock.accept()
            print('Client connected', end='')

            username = client.recv(1024).decode()
            print(f', Name:  {username}')

            new_player = Player(
                username=username,
                ID=currentID,
                sock=client,
            )

            self._players.append(new_player)

            self._threads.append(
                threading.Thread(
                    target=self.handle_player,
                    args=(new_player,)
                )
            )

            currentID += 1
            if len(self._players) == 1:
                break

    def handle_player(self, player: Player):
        while True:
            message = pickle.loads(player.client.recv(1024))
            if message['status'] == Player_Commands.QUIT:
                player.client.close()
                print(f'Client disconnected, name: {player.username}')
                break

            for key, val in message.items():
                if val is not None:
                    self._requests.append(
                        Request(val, player.ID)
                    )
                    print(val)

            self._requests.append(
                Request(message, )
            )

    def mainloop(self) -> None:
        print('In mainloop')
        for player in self._players:
            player.thread.start()
        while True:
            if self._requests:
                # print(self._requests)
                self._requests.clear()


def main():
    server = Online_Game_Server()
    server.mainloop()


if __name__ == "__main__":
    main()
