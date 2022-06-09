import pickle
import socket
import threading
import pygame
from dataclasses import dataclass
from time import sleep

from enums import Directions, Player_Commands, Game_Objects
from sprites import Player as Player_Sprite


@dataclass
class Player:
    username: str
    ID: int
    sock: socket.socket


@dataclass
class Request:
    type: Player_Commands
    player_ID: int


class Online_Game_Server:
    def __init__(self, IP, port) -> None:
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_sock.bind((IP, port))
        print('Server is up and running')

        self._players = {}
        self._threads: list[threading.Thread] = []
        self._requests = []

        self._player_sprites = {}

        self._sprites_to_send = []

        self._get_clients()

    def _get_clients(self) -> None:
        """
        Listens to connections and adds them to the players dict
        Creates a thread to handle them and adds it to the threads list
        """
        currentID = 0
        while True:
            self.server_sock.listen()
            client, client_address = self.server_sock.accept()
            print('Client connected', end='')

            username = client.recv(1024).decode()
            print(f', Name:  {username}')

            new_player = Player(
                username=username,
                ID=currentID,
                sock=client,
            )

            self._players[currentID] = new_player

            self._threads.append(
                threading.Thread(
                    target=self._handle_player,
                    args=(new_player,)
                )
            )

            self._player_sprites[currentID] = Player_Sprite(
                currentID,
                (0, 0)
            )

            currentID += 1
            if len(self._players) == 2:
                break

    def _handle_player(self, player: Player):
        """
        Handles the player and recieves all data sent by them
        Puts the data in the requests list
        ...
        :param player: the player to handle
        """
        try:
            while True:
                message = pickle.loads(player.sock.recv(1024))
                if message['status'] == Player_Commands.QUIT:
                    player.sock.close()
                    print(f'Client disconnected, name: {player.username}')
                    break

                for key, val in message.items():
                    if val is not None:
                        self._requests.append(
                            Request(val, player.ID)
                        )
                        print(val)

                self._requests.append(
                    Request(message, player.ID)
                )
        except ConnectionResetError:
            print(f'Player {player.username} has disconnected')
            self._players.pop(player.ID)

    def _send_data(self, client: socket.socket, data: dict):
        """
        Sends data to the client
        The data is a dictionary of all sprites and their location
        ...
        :param client: the client to send to
        :param data: the data to send
        """
        ser_data = pickle.dumps(data)
        client.send(ser_data)

    def mainloop(self) -> None:
        """
        The mainloop of the program, call to run it
        """
        print('In mainloop')
        for t in self._threads:
            t.start()
        while True:
            if self._requests:
                # for request in self._requests:
                #     print(request.type)
                for request in self._requests:
                    player_ID = request.player_ID
                    match request.type:
                        case Player_Commands.MOVE_UP:
                            self._player_sprites[player_ID].change_y_speed(-10)
                        case Player_Commands.MOVE_DOWN:
                            self._player_sprites[player_ID].change_y_speed(10)
                        case Player_Commands.MOVE_LEFT:
                            self._player_sprites[player_ID].change_x_speed(-10)
                        case Player_Commands.MOVE_RIGHT:
                            self._player_sprites[player_ID].change_x_speed(10)

                        case Player_Commands.STOP_MOVE_UP:
                            self._player_sprites[player_ID].change_y_speed(10)
                        case Player_Commands.STOP_MOVE_DOWN:
                            self._player_sprites[player_ID].change_y_speed(-10)
                        case Player_Commands.STOP_MOVE_LEFT:
                            self._player_sprites[player_ID].change_x_speed(10)
                        case Player_Commands.STOP_MOVE_RIGHT:
                            self._player_sprites[player_ID].change_x_speed(-10)

                self._requests.clear()  # clear events list after iterating through them
            for ID, sprite in self._player_sprites.items():
                sprite.update()

            for player_ID, sprite in self._player_sprites.items():
                self._sprites_to_send.append(
                    (Game_Objects.Player, sprite.get_coords())
                )

            for ID, player in self._players.items():
                print(f'Sending data to {player.username}')
                self._send_data(player.sock, self._sprites_to_send)
                self._sprites_to_send.clear()

            sleep(1/30)


def main():
    server = Online_Game_Server('192.168.68.131', 3333)
    server.mainloop()


if __name__ == "__main__":
    main()
