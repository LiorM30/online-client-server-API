from enum import Enum
from dataclasses import dataclass


class Game_Packet_Type(str, Enum):
    RECIEVE_SPRITES = 'recieve sprites'
    PLAYER_INPUTS = 'player inputs'


@dataclass
class Game_Packet():
    type: Game_Packet_Type
    data: dict = None
