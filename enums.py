from enum import Enum


class Player_Commands(str, Enum):
    MOVE_UP = 'move up'
    MOVE_DOWN = 'move down'
    MOVE_LEFT = 'move left'
    MOVE_RIGHT = 'move right'

    STOP_MOVE_UP = 'stop move up'
    STOP_MOVE_DOWN = 'stop move down'
    STOP_MOVE_LEFT = 'stop move left'
    STOP_MOVE_RIGHT = 'stop move right'

    SHOOT_UP = 'shoot up'
    SHOOT_DOWN = 'shoot down'
    SHOOT_LEFT = 'shoot left'
    SHOOT_RIGHT = 'shoot right'

    STOP_SHOOT_UP = 'stop shoot up'
    STOP_SHOOT_DOWN = 'stop shoot down'
    STOP_SHOOT_LEFT = 'stop shoot left'
    STOP_SHOOT_RIGHT = 'stop shoot right'

    PLAYER_QUIT = 'player quit'
    QUIT = 'quit'
