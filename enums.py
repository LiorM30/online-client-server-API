from enum import Enum


class Player_Commands(str, Enum):  # inhereting from str to make serializeble
    MOVE_UP = 'move up'
    MOVE_DOWN = 'move down'
    MOVE_LEFT = 'move left'
    MOVE_RIGHT = 'move right'

    STOP_MOVE_UP = 'stop move up'
    STOP_MOVE_DOWN = 'stop move down'
    STOP_MOVE_LEFT = 'stop move left'
    STOP_MOVE_RIGHT = 'stop move right'

    QUIT = 'quit'


class Directions(Enum):
    UP = 'up'
    DOWN = 'down'
    LEFT = 'left'
    RIGHT = 'right'


class Game_Objects(str, Enum):
    Player = 'player'


class Game_Comm_API(str, Enum):
    REQUEST_SPRITES = 'request sprites'
