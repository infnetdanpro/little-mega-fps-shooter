import threading

import sys

from ursina import Ursina, window, color, Sky, Vec3, destroy

from game.bullet import Bullet
from game.enemy import Enemy
from game.ground import Ground
from game.map import Map
from game.network import Network
from game.player import Player

if __name__ == '__main__':

    username = None
    while True:
        username = input("Input username: ")
        if username:
           break

    while True:
        server_ip = '127.0.0.1'
        server_port = 27020

        n = Network(server_ip=server_ip, server_port=server_port, username=username)
        n.settimeout(5)
        error_occured = False
        try:
            n.connect()
        except Exception as e:
            error_occured = True
            print(e)
        finally:
            n.settimeout(None)
        if not error_occured:
            break

    app = Ursina()

    window.color = color.rgb(0, 0, 0)
    window.title = "MegaFPS Shooter"
    window.exit_button = False
    sky = Sky()
    ground = Ground()
    map = Map()

    player = Player(position=Vec3(0.516542, 0, -35.4379))
    enemies = []
    prev_pos = player.world_position
    prev_dir = player.world_rotation_y

    def receive():
        while True:
            try:
                msg = n.receive_info()
            except Exception as e:
                print(e)
                continue

            if not msg:
                print('Empty info from server, exiting')
                sys.exit()

            if msg['object'] == 'player':
                enemy_id = msg['id']

                if msg['joined'] == 1:
                    new_enemy = Enemy(Vec3(*msg['position']), enemy_id, msg['username'])
                    new_enemy.health = msg['health']
                    enemies.append(new_enemy)
                    continue

                enemy: Enemy = None

                for e in enemies:
                    if e.id == enemy_id:
                        enemy = e
                        break

                if not enemy:
                    continue

                if msg['left'] == 1:
                    enemies.remove(enemy)
                    destroy(enemy)
                    continue

                enemy.world_position = Vec3(*msg['position'])
                enemy.rotation_y = msg['rotation']
            elif msg['object'] == 'bullet':
                b_pos = Vec3(*msg['position'])
                b_dir = msg['direction']
                b_x_dir = msg['x_direction']
                b_damage = msg['damage']
                new_bullet = Bullet(b_pos, b_dir, b_x_dir, n, b_damage, slave=True)
                destroy(new_bullet, delay=2)
            elif msg['object'] == 'health_update':
                enemy_id = msg['id']

                enemy: Enemy = None

                if enemy_id == n.id:
                    enemy = player
                else:
                    for e in enemies:
                        if e.id == enemy_id:
                            enemy = e
                            break

                if not enemy:
                    continue

                enemy.health = msg['health']
    def update():
        if player.health > 0:
            global prev_pos, prev_dir

            if prev_pos != player.world_position or prev_dir != player.world_rotation_y:
                n.send_player(player=player)

            prev_pos = player.world_position
            prev_dir = player.world_rotation_y

    def input(key):
        if key == 'left mouse down' and player.health > 0:
            b_pos = player.position + Vec3(0, 2, 0)
            bullet = Bullet(b_pos, player.world_rotation_y, player.camera_pivot.world_rotation_x, n)
            n.send_bullet(bullet=bullet)
            destroy(bullet, delay=2)

    msg_thread = threading.Thread(target=receive, daemon=True)
    msg_thread.start()
    app.run()
