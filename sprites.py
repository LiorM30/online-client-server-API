from asyncio.constants import SENDFILE_FALLBACK_READBUFFER_SIZE
import pygame


from enums import Player_Commands, Directions


class Player(pygame.sprite.Sprite):
    def __init__(self, ID: int, coords: tuple[int, int]) -> None:
        super().__init__()

        self._ID = ID
        self._coords = coords

        self._image = pygame.Surface((50, 50))
        self._image.fill((255, 255, 255))
        self.rect = self._image.get_rect()
        self.rect.center = coords

        self._x_speed = 0  # the sprite's movement speeds
        self._y_speed = 0

    def update(self):
        self._move()

    def _move(self):
        self.rect.y += self._y_speed
        self.rect.x += self._x_speed

    def change_y_speed(self, speed):
        self._y_speed += speed

    def change_x_speed(self, speed):
        self._x_speed += speed

    def get_coords(self) -> tuple[int, int]:
        return (self.rect.x, self.rect.y)
