import socket
from _thread import *
from board import Board
import pickle
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
server = host_ip
port = 5555

server_ip = socket.gethostbyname(server)

try:
    s.bind((server, port))

except socket.error as e:
    print(str(e))

s.listen()
print("[Bắt đầu] Đợi người chơi kết nối đến server")
connections = 0
games = {0:Board(8, 8)}
specs = 0
def threaded_client(conn, game, spec=False):
    global pos, games, currentId, connections, specs
    if not spec:
        name = None
        bo = games[game]
        if connections % 2 == 0:
            currentId = "w"
        else:
            currentId = "b"
        bo.start_user = currentId
        # Pickle the object and send it to the server
        data_string = pickle.dumps(bo)
        if currentId == "b":
            bo.ready = True
            bo.startTime = time.time()

        conn.send(data_string)
        connections += 1
        while True:
            if game not in games:
                break
            try:
                d = conn.recv(8192 * 3)
                data = d.decode("utf-8")
                if not d:
                    break
                else:
                    if data.count("select") > 0:
                        all = data.split(" ")
                        col = int(all[1])
                        row = int(all[2])
                        color = all[3]
                        bo.select(col, row, color)
                    if data == "winner b":
                        bo.winner = "b"
                        print("[GAME] Player b won in game", game)
                    if data == "winner w":
                        bo.winner = "w"
                        print("[GAME] Player w won in game", game)
                    if data == "update moves":
                        bo.update_moves()
                    if data.count("name") == 1:
                        name = data.split(" ")[1]
                        if currentId == "b":
                            bo.p2Name = name
                        elif currentId == "w":
                            bo.p1Name = name
                    if bo.ready:
                        if bo.turn == "w":
                            bo.time1 = 900 - (time.time() - bo.startTime) - bo.storedTime1
                        else:
                            bo.time2 = 900 - (time.time() - bo.startTime) - bo.storedTime2
                    sendData = pickle.dumps(bo)
                conn.sendall(sendData)
            except Exception as e:
                print(e)
        connections -= 1
        try:
            del games[game]
            print("[Trò chơi]", game, "kết thúc")
        except:
            pass
        print("[Ngắt kết nối] bạn ", name, " đã rời khỏi trò chơi", game)
        conn.close()
        
while True:
  
    if connections < 6:
        conn, addr = s.accept()
        spec = False
        g = -1
        print("[Kết nối] Kết nối mới")

        for game in games.keys():
            if games[game].ready == False:
                g=game

        if g == -1:
            try:
                g = list(games.keys())[-1]+1
                games[g] = Board(8,8)
            except:
                g = 0
                games[g] = Board(8,8)
        print("[DATA] Số lượng người chơi đã kết nối:", connections+1)
        start_new_thread(threaded_client, (conn,g,spec))
