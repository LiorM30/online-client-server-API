import socket
import pickle
import pygame
import io

from enums import Game_Objects, Player_Commands


class Online_Game_Client:
    def __init__(self, server_ip, server_port) -> None:
        self.client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_sock.connect((server_ip, server_port))
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

        player_sprite = pygame.image.load('assets\\player.png')
        player_sprite = pygame.transform.scale(
            player_sprite, (50, 50)
        )

        self._all_sprites = {
            Game_Objects.Player: player_sprite
        }

    def mainloop(self):
        """
        The mainloop of the program, call to start it
        """
        while self._running:
            inputs = {  # all command types
                'shooting': None,
                'move x': None,
                'move y': None,
                'status': None
            }
            self._clock.tick(30)  # setting game FPS

            for event in pygame.event.get():
                # this one checks for the window being closed
                if event.type == pygame.QUIT:
                    inputs['status'] = Player_Commands.QUIT
                    pygame.quit()

                if event.type == pygame.KEYDOWN:  # key-press events
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
            
            # keys = pygame.key.get_pressed()
            # if not (keys[pygame.K_a] and keys[pygame.K_d]):
            #     if keys[pygame.K_a]:
            #         inputs['move x'] = Player_Commands.MOVE_LEFT
            #     elif keys[pygame.K_d]:
            #         inputs['move x'] = Player_Commands.MOVE_RIGHT
            # if not (keys[pygame.K_w] and keys[pygame.K_s]):
            #     if keys[pygame.K_w]:
            #         inputs['move x'] = Player_Commands.MOVE_UP
            #     elif keys[pygame.K_s]:
            #         inputs['move x'] = Player_Commands.MOVE_DOWN

            if inputs['status'] == Player_Commands.QUIT:  # if player quits, stop game
                self._running = False
            if not all(value is None for value in inputs.values()):
                self._send_data(inputs)

            # print('Getting sprites')
            sprites_to_load = pickle.loads(self.client_sock.recv(4096))
            self._screen.fill((0, 0, 0))
            self._render_sprites(sprites_to_load)
            pygame.display.flip()

    def _send_data(self, data: dict) -> None:
        """
        Sends data to the server
        The data is a dictionary of all inputs the player did
        ...
        :param data: the data to send
        """
        ser_data = pickle.dumps(data)
        self.client_sock.send(ser_data)

    def _render_sprites(self, sprites: list):
        # print(f'Rendering sprites')
        for sprite, coords in sprites:
            self._draw_object(sprite, coords)

    def _draw_object(self, object: Game_Objects, coords: tuple[int, int]) -> None:
        self._screen.blit(self._all_sprites[object], coords)




def main():
    client = Online_Game_Client('192.168.68.131', 3333)
    client.mainloop()


if __name__ == "__main__":
    main()
