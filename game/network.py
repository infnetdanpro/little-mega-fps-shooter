import socket

import ujson as json
from game.bullet import Bullet
from game.enemy import Enemy
from game.player import Player


class Network:
    def __init__(self, server_ip: str, server_port: int, username: str):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = server_ip
        self.port = server_port
        self.username = username
        self.recv_size = 4096
        self.id = 0

    def settimeout(self, value):
        self.client.settimeout(value)

    def connect(self):
        self.client.connect((self.addr, self.port))
        self.id = self.client.recv(self.recv_size).decode("utf-8")
        self.username = self.username.replace(',', '')
        self.client.send(self.username.encode("utf-8"))

    def receive_info(self) -> str:
        msg = None
        try:
            msg = self.client.recv(self.recv_size).decode('utf-8')
        except socket.error as e:
            print(e)

        if not msg:
            return None

        return json.loads(msg)

    def send_player(self, player: Player):
        player_info = json.dumps({
            'id': self.id,
            'object': 'player',
            'username': self.username,
            'position': (player.world_x, player.world_y, player.world_z),
            # 'rotation': player.rotation,
            'health': player.health,
            'joined': 0,
            'left': 0
        })
        try:
            self.client.send(player_info.encode('utf-8'))
        except socket.error as e:
            print(e)

    def send_bullet(self, bullet: Bullet):
        bullet_info = json.dumps({
            'object': 'bullet',
            'position': (bullet.world_x, bullet.world_y, bullet.world_z),
            'damage': bullet.damage,
            'direction': bullet.direction,
            'x_direction': bullet.x_direction
        })
        try:
            self.client.send(bullet_info.encode('utf-8'))
        except socket.error as e:
            print(e)

    def send_health(self, player: Enemy):
        health_info = json.dumps({
            'object': 'health_update',
            'id': player.id,
            'health': player.health
        })
        try:
            self.client.send(health_info.encode('utf-8'))
        except socket.error as e:
            print(e)
