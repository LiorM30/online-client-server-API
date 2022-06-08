import socket
import pickle
import pygame

from enums import Player_Commands


class Online_Game_Client:
    SERVER_PORT = 3333
    SERVER_IP = '172.16.17.115'

    def __init__(self) -> None:
        self.client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_sock.connect((self.SERVER_IP, self.SERVER_PORT))
        print('client connected')

        self._username = input('enter your username:  ')
        self.client_sock.send(self._username.encode())

        pygame.init()
        self._screen = pygame.display.set_mode(
            (400, 400)
        )
        pygame.display.set_caption('Tanks')
        pygame.key.set_repeat()  # key presses will not repeat

        self._clock = pygame.time.Clock()

        self._running = True

    def mainloop(self):
        while self._running:
            inputs = {  # all command types
                'shooting': None,
                'move x': None,
                'move y': None,
                'status': None
            }
            self._clock.tick(60)

            for event in pygame.event.get():
                # this one checks for the window being closed
                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.KEYDOWN:
                    match event.key:
                        case pygame.K_LEFT:
                            inputs['shooting'] = Player_Commands.SHOOT_LEFT
                        case pygame.K_RIGHT:
                            inputs['shooting'] = Player_Commands.SHOOT_RIGHT
                        case pygame.K_UP:
                            inputs['shooting'] = Player_Commands.SHOOT_UP
                        case pygame.K_DOWN:
                            inputs['shooting'] = Player_Commands.SHOOT_DOWN
                        case pygame.K_a:
                            inputs['move x'] = Player_Commands.MOVE_LEFT
                        case pygame.K_d:
                            inputs['move x'] = Player_Commands.MOVE_RIGHT
                        case pygame.K_w:
                            inputs['move y'] = Player_Commands.MOVE_UP
                        case pygame.K_s:
                            inputs['move y'] = Player_Commands.MOVE_DOWN
                        case pygame.K_ESCAPE:
                            inputs['status'] = Player_Commands.QUIT
                if event.type == pygame.KEYUP:
                    match event.key:
                        case pygame.K_LEFT:
                            inputs['shooting'] = Player_Commands.STOP_SHOOT_LEFT
                        case pygame.K_RIGHT:
                            inputs['shooting'] = Player_Commands.STOP_SHOOT_RIGHT
                        case pygame.K_UP:
                            inputs['shooting'] = Player_Commands.STOP_SHOOT_UP
                        case pygame.K_DOWN:
                            inputs['shooting'] = Player_Commands.STOP_SHOOT_DOWN
                        case pygame.K_a:
                            inputs['move x'] = Player_Commands.STOP_MOVE_LEFT
                        case pygame.K_d:
                            inputs['move x'] = Player_Commands.STOP_MOVE_RIGHT
                        case pygame.K_w:
                            inputs['move y'] = Player_Commands.STOP_MOVE_UP
                        case pygame.K_s:
                            inputs['move y'] = Player_Commands.STOP_MOVE_DOWN
            if inputs['status'] == Player_Commands.QUIT:
                self._running = False
            if not all(value is None for value in inputs.values()):
                self._send_data(inputs)

    def _send_data(self, data: dict) -> None:
        ser_data = pickle.dumps(data)
        self.client_sock.send(ser_data)


def main():
    client = Online_Game_Client()
    client.mainloop()


if __name__ == "__main__":
    main()
