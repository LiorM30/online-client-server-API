import socket
import threading


class Online_Game_API:
    def __init__(self) -> None:
        self._clients = []
