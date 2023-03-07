import socket
import uuid

import time
import threading
import ujson as json


ADDR = "0.0.0.0"
PORT = 27020
MAX_PLAYERS = 10
MSG_SIZE = 4096

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((ADDR, PORT))
s.listen(MAX_PLAYERS)

players = {}


def generate_player_id(player_list: dict) -> str:
    return str(str(uuid.uuid4()))


def handle_msg(identifier: str):
    client_info = players[identifier]
    conn: socket.socket = client_info["socket"]
    username = client_info["username"]

    while True:
        try:
            msg = conn.recv(MSG_SIZE)
        except ConnectionResetError:
            break

        if not msg:
            break

        msg_decoded = msg.decode("utf-8")
        try:
            msg_data = json.loads(msg_decoded)
        except json.JSONDecodeError:
            print(msg_decoded)

        if object == 'player':
            players[identifier]["position"] = msg_data['position']
            players[identifier]["rotation"] = msg_data['rotation']
            players[identifier]["health"] = msg_data['health']

        # tell all other players about player moving
        for player_id in players:
            if player_id == identifier:
                continue
            player_info = players[player_id]
            player_conn: socket.socket = player_info["socket"]

            try:
                # TODO: do it via workers?:)
                player_conn.sendall(msg_decoded.encode('utf-8'))
            except OSError:
                pass


    for player_id in players:
        if player_id == identifier:
            continue
        player_info = players[player_id]
        player_conn: socket.socket = player_info["socket"]

        try:
            # identifier, object, username, position, rotation, health, joined, left
            player_conn.send(json.dumps({
                'id': identifier,
                'object': 'player',
                'joined': 0,
                'left': 1,
            }).encode('utf-8'))
            print(f'Player {username} with id: {identifier} has left the game...')
            del players[identifier]
            conn.close()
        except OSError:
            pass


def main():
    print('ServerD started')

    while True:
        conn, addr = s.accept()
        new_player_id = generate_player_id(player_list=players)
        conn.send(new_player_id.encode('utf-8'))
        username = conn.recv(MSG_SIZE).decode("utf-8")
        new_player_info = {'socket': conn, "username": username, "position": (0, 1, 0), "rotation": 0, "health": 100}

        # send to other players new info about new player
        for player_id in players:
            if player_id == new_player_id:
                continue
            player_conn = players[player_id]["socket"]
            try:
                # id,object,username,position,health,joined,left
                player_conn.send(json.dumps({
                    'id': new_player_id,
                    'object': 'player',
                    'username': new_player_info['username'],
                    'position': new_player_info['position'],
                    'health': new_player_info['health'],
                    'joined': 1,
                    'left': 0
                }).encode('utf-8'))
            except OSError:
                pass

        # send to the new player info about all other players
        for player_id in players:
            if player_id == new_player_id:
                continue
            player_info = players[player_id]
            try:
                conn.send(json.dumps({
                    'id': player_id,
                    'object': 'player',
                    'username': player_info['username'],
                    'position': player_info['position'],
                    'health': player_info['health'],
                    'joined': 1,
                    'left': 0
                }).encode('utf-8'))
                time.sleep(0.01)
            except OSError:
                pass

        players[new_player_id] = new_player_info

        msg_thread = threading.Thread(target=handle_msg, args=(new_player_id,), daemon=True)
        msg_thread.start()

        print(f'New connection from {addr}, assigned ID: {new_player_id}...')

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    except SystemExit:
        pass
    finally:
        print('Exiting')
        s.close()