from enum import Enum


class Player_Commands(Enum):
    MOVE_UP = 'move up'
    MOVE_DOWN = 'move down'
    MOVE_LEFT = 'move left'
    MOVE_RIGHT = 'move right'

    SHOOT_UP = 'shoot up'
    SHOOT_DOWN = 'shoot down'
    SHOOT_LEFT = 'shoot left'
    SHOOT_RIGHT = 'shoot right'

    QUIT = 'quit'
