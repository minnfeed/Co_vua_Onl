from piece import Bishop
from piece import King
from piece import Rook
from piece import Pawn
from piece import Queen
from piece import Knight
import time
import pygame


class Board:
    rect = (113, 113, 525, 525)
    startX = rect[0]
    startY = rect[1]
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols

        self.ready = False

        self.last = None

        self.copy = True

        self.board = [[0 for x in range(8)] for _ in range(rows)]

        self.board[0][0] = Rook(0, 0, "b")
        self.board[0][1] = Knight(0, 1, "b")
        self.board[0][2] = Bishop(0, 2, "b")
        self.board[0][3] = Queen(0, 3, "b")
        self.board[0][4] = King(0, 4, "b")
        self.board[0][5] = Bishop(0, 5, "b")
        self.board[0][6] = Knight(0, 6, "b")
        self.board[0][7] = Rook(0, 7, "b")

        self.board[1][0] = Pawn(1, 0, "b")
        self.board[1][1] = Pawn(1, 1, "b")
        self.board[1][2] = Pawn(1, 2, "b")
        self.board[1][3] = Pawn(1, 3, "b")
        self.board[1][4] = Pawn(1, 4, "b")
        self.board[1][5] = Pawn(1, 5, "b")
        self.board[1][6] = Pawn(1, 6, "b")
        self.board[1][7] = Pawn(1, 7, "b")

        self.board[7][0] = Rook(7, 0, "w")
        self.board[7][1] = Knight(7, 1, "w")
        self.board[7][2] = Bishop(7, 2, "w")
        self.board[7][3] = Queen(7, 3, "w")
        self.board[7][4] = King(7, 4, "w")
        self.board[7][5] = Bishop(7, 5, "w")
        self.board[7][6] = Knight(7, 6, "w")
        self.board[7][7] = Rook(7, 7, "w")

        self.board[6][0] = Pawn(6, 0, "w")
        self.board[6][1] = Pawn(6, 1, "w")
        self.board[6][2] = Pawn(6, 2, "w")
        self.board[6][3] = Pawn(6, 3, "w")
        self.board[6][4] = Pawn(6, 4, "w")
        self.board[6][5] = Pawn(6, 5, "w")
        self.board[6][6] = Pawn(6, 6, "w")
        self.board[6][7] = Pawn(6, 7, "w")

        self.p1Name = "Player 1"
        self.p2Name = "Player 2"
        self.turn = "w"
        self.time1 = 900
        self.time2 = 900
        self.storedTime1 = 0
        self.storedTime2 = 0
        self.winner = None
        self.startTime = time.time()

    def update_moves(self):
        # Duyệt qua từng hàng trên bảng
        for i in range(self.rows):
            # Duyệt qua từng cột trong hàng hiện tại
            for j in range(self.cols):
                # Kiểm tra nếu ô hiện tại không trống (không chứa giá trị `0`)
                if self.board[i][j] != 0:
                    # Gọi phương thức `update_valid_moves` trên đối tượng trong ô hiện tại
                    # Truyền toàn bộ bảng làm đối số cho phương thức này
                    self.board[i][j].update_valid_moves(self.board)

    def draw(self, win, color):
        if self.last and color == self.turn:
            y, x = self.last[0]
            y1, x1 = self.last[1]

            xx = (4 - x) +round(self.startX + (x * self.rect[2] / 8))
            yy = 3 + round(self.startY + (y * self.rect[3] / 8))
            pygame.draw.circle(win, (0,0,255), (xx+32, yy+30), 34, 4)
            xx1 = (4 - x) + round(self.startX + (x1 * self.rect[2] / 8))
            yy1 = 3+ round(self.startY + (y1 * self.rect[3] / 8))
            pygame.draw.circle(win, (0, 0, 255), (xx1 + 32, yy1 + 30), 34, 4)

        s = None
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != 0:
                    self.board[i][j].draw(win, color)
                    if self.board[i][j].isSelected:
                        s = (i, j)

    def draw(self, win, color):
        # Kiểm tra nếu có nước đi cuối cùng và màu sắc trùng với lượt đi hiện tại
        if self.last and color == self.turn:
            # Lấy tọa độ của nước đi cuối cùng và nước đi trước đó
            y, x = self.last[0]
            y1, x1 = self.last[1]

            # Tính toán tọa độ vẽ hình tròn tại nước đi cuối cùng
            xx = (4 - x) + round(self.startX + (x * self.rect[2] / 8))
            yy = 3 + round(self.startY + (y * self.rect[3] / 8))
            # Vẽ hình tròn thể hiện nước đi cuối cùng
            pygame.draw.circle(win, (0, 0, 255), (xx + 32, yy + 30), 34, 4)

            # Tính toán tọa độ vẽ hình tròn tại nước đi trước đó
            xx1 = (4 - x) + round(self.startX + (x1 * self.rect[2] / 8))
            yy1 = 3 + round(self.startY + (y1 * self.rect[3] / 8))
            # Vẽ hình tròn thể hiện nước đi trước đó
            pygame.draw.circle(win, (0, 0, 255), (xx1 + 32, yy1 + 30), 34, 4)

        # Biến tạm để lưu trữ tọa độ của ô đang được chọn (nếu có)
        s = None
        # Duyệt qua từng hàng trên bảng
        for i in range(self.rows):
            # Duyệt qua từng cột trong hàng hiện tại
            for j in range(self.cols):
                # Kiểm tra nếu ô hiện tại không trống
                if self.board[i][j] != 0:
                    # Vẽ đối tượng trong ô hiện tại lên màn hình
                    self.board[i][j].draw(win, color)
                    # Nếu ô đang được chọn, lưu lại tọa độ của ô đó
                    if self.board[i][j].isSelected:
                        s = (i, j)

    def is_checked(self, color):
        # Cập nhật lại các nước đi hợp lệ
        self.update_moves()
        # Lấy danh sách các nước đi nguy hiểm đối với một màu cụ thể
        danger_moves = self.get_danger_moves(color)
        # Khởi tạo biến lưu vị trí của quân vua
        king_pos = (-1, -1)
        # Duyệt qua từng hàng trên bảng
        for i in range(self.rows):
            # Duyệt qua từng cột trong hàng hiện tại
            for j in range(self.cols):
                # Kiểm tra nếu ô hiện tại không trống
                if self.board[i][j] != 0:
                    # Kiểm tra nếu ô hiện tại là quân vua và thuộc màu của bên cần kiểm tra
                    if self.board[i][j].king and self.board[i][j].color == color:
                        # Lưu lại vị trí của quân vua
                        king_pos = (j, i)

        # Kiểm tra xem vị trí của quân vua có trong danh sách các nước đi nguy hiểm hay không
        if king_pos in danger_moves:
            # Nếu có, tức là quân vua bị chiếu
            return True

        # Nếu không, tức là quân vua không bị chiếu
        return False

    def select(self, col, row, color):
        # Biến này sẽ được sử dụng để xác định liệu có thay đổi (chọn một ô mới) hay không
        changed = False
        # Lưu trữ tọa độ của ô trước đó được chọn
        prev = (-1, -1)
        # Duyệt qua từng hàng trên bảng
        for i in range(self.rows):
            # Duyệt qua từng cột trong hàng hiện tại
            for j in range(self.cols):
                # Kiểm tra nếu ô hiện tại không trống
                if self.board[i][j] != 0:
                    # Kiểm tra nếu ô hiện tại đã được chọn trước đó
                    if self.board[i][j].selected:
                        # Lưu lại tọa độ của ô được chọn trước đó
                        prev = (i, j)

        # if piece
        # Nếu ô được chọn là ô trống và đã có ô được chọn trước đó
        if self.board[row][col] == 0 and prev != (-1, -1):
            # Lấy danh sách các nước đi của quân cờ được chọn trước đó
            moves = self.board[prev[0]][prev[1]].move_list
            # Kiểm tra xem ô đích có trong danh sách nước đi hợp lệ không
            if (col, row) in moves:
                # Nếu có, di chuyển quân cờ
                changed = self.move(prev, (row, col), color)


        else:

            if prev == (-1, -1):

                # Nếu chưa có ô nào được chọn trước đó, chọn ô hiện tại

                self.reset_selected()

                if self.board[row][col] != 0:
                    self.board[row][col].selected = True
            else:
                # Nếu đã có ô được chọn trước đó
                if self.board[prev[0]][prev[1]].color != self.board[row][col].color:
                    # Nếu quân cờ ở ô được chọn trước đó có thể di chuyển đến ô hiện tại
                    moves = self.board[prev[0]][prev[1]].move_list
                    if (col, row) in moves:
                        # Thực hiện di chuyển quân cờ
                        changed = self.move(prev, (row, col), color)
                    # Nếu quân cờ ở ô hiện tại cùng màu với lượt đi hiện tại
                    if self.board[row][col].color == color:
                        # Chọn ô hiện tại
                        self.board[row][col].selected = True
                else:
                    # Nếu quân cờ ở ô hiện tại cùng màu với lượt đi hiện tại
                    if self.board[row][col].color == color:
                        # Kiểm tra điều kiện để thực hiện phép Nhập Thú (castling)
                        if self.board[prev[0]][prev[1]].moved == False and self.board[prev[0]][prev[1]].rook and \
                                self.board[row][col].king and col != prev[1] and prev != (-1, -1):
                            # Khởi tạo biến để kiểm tra điều kiện phép Nhập Thú
                            castle = True
                            # Nếu quân cờ vua di chuyển về phía bên trái
                            if prev[1] < col:
                                # Kiểm tra xem có quân cờ nào ở giữa không
                                for j in range(prev[1] + 1, col):
                                    if self.board[row][j] != 0:
                                        castle = False
                                # Nếu không có quân cờ nào ở giữa, thực hiện phép Nhập Thú
                                if castle:
                                    changed = self.move(prev, (row, 3), color)
                                    changed = self.move((row, col), (row, 2), color)
                                # Nếu không thực hiện được, chọn ô hiện tại
                                if not changed:
                                    self.board[row][col].selected = True
                            else:
                                # Nếu quân cờ vua di chuyển về phía bên phải
                                for j in range(col + 1, prev[1]):
                                    # Kiểm tra xem có quân cờ nào ở giữa không
                                    if self.board[row][j] != 0:
                                        castle = False
                                # Nếu không có quân cờ nào ở giữa, thực hiện phép Nhập Thú
                                if castle:
                                    changed = self.move(prev, (row, 6), color)
                                    changed = self.move((row, col), (row, 5), color)
                                # Nếu không thực hiện được, chọn ô hiện tại
                                if not changed:
                                    self.board[row][col].selected = True
                        else:
                            # Nếu không thực hiện phép Nhập Thú, chọn ô hiện tại
                            self.board[row][col].selected = True

    def reset_selected(self):
        # Duyệt qua từng hàng trên bảng
        for i in range(self.rows):
            # Duyệt qua từng cột trong hàng hiện tại
            for j in range(self.cols):
                # Kiểm tra nếu ô hiện tại không trống
                if self.board[i][j] != 0:
                    # Đặt trạng thái "được chọn" của ô hiện tại thành False
                    self.board[i][j].selected = False

    # Hàm kiểm tra chiếu bí
    def check_mate(self, color):
        # Kiểm tra xem bên đang ở trong tình trạng bị chiếu hay không
        if self.is_checked(color):
            # Khởi tạo biến để lưu vị trí của quân vua
            king = None
            for i in range(self.rows):
                for j in range(self.cols):
                    # Tìm quân vua của bên đang kiểm tra
                    if self.board[i][j] != 0:
                        if self.board[i][j].king and self.board[i][j].color == color:
                            king = self.board[i][j]
            # Nếu quân vua của bên đang kiểm tra tồn tại
            if king is not None:
                # Lấy danh sách các nước đi hợp lệ của quân vua
                valid_moves = king.valid_moves(self.board)

                # Lấy danh sách các nước đi nguy hiểm đối với bên đang kiểm tra
                danger_moves = self.get_danger_moves(color)

                # Khởi tạo biến để đếm số nước đi nguy hiểm
                danger_count = 0

                # Đếm số nước đi hợp lệ mà cũng là nước đi nguy hiểm
                for move in valid_moves:
                    if move in danger_moves:
                        danger_count += 1
                # Kiểm tra xem số nước đi nguy hiểm có bằng tổng số nước đi hợp lệ hay không
                return danger_count == len(valid_moves)

        # Nếu không bị chiếu, trả về False
        return False

    def move(self, start, end, color):
        # Lưu trạng thái trước đó của việc bị chiếu
        checkedBefore = self.is_checked(color)
        # Biến này để theo dõi xem nước đi có thực sự thay đổi không
        changed = True
        # Tạo một bản sao của bảng cờ để thực hiện nước đi
        nBoard = self.board[:]
        # Nếu quân cờ là tốt và đang di chuyển lần đầu tiên, đặt trạng thái first thành False
        if nBoard[start[0]][start[1]].pawn:
            nBoard[start[0]][start[1]].first = False

        # Di chuyển quân cờ từ ô bắt đầu đến ô kết thúc
        nBoard[start[0]][start[1]].change_pos((end[0], end[1]))
        nBoard[end[0]][end[1]] = nBoard[start[0]][start[1]]
        nBoard[start[0]][start[1]] = 0
        self.board = nBoard

        # Kiểm tra xem việc di chuyển quân cờ đã gây ra tình trạng chiếu hay không
        # hoặc nếu trước đó đã bị chiếu
        if self.is_checked(color) or (checkedBefore and self.is_checked(color)):
            # Nếu di chuyển quân cờ gây ra chiếu hoặc không loại bỏ tình trạng chiếu,
            # đặt biến changed thành False và hoàn tác nước đi
            changed = False
            nBoard = self.board[:]
            # Nếu quân cờ là tốt và đang di chuyển lần đầu tiên, đặt trạng thái first thành True
            if nBoard[end[0]][end[1]].pawn:
                nBoard[end[0]][end[1]].first = True

            # Hoàn tác nước đi
            nBoard[end[0]][end[1]].change_pos((start[0], start[1]))
            nBoard[start[0]][start[1]] = nBoard[end[0]][end[1]]
            nBoard[end[0]][end[1]] = 0
            self.board = nBoard
        else:
            # Nếu không gây ra tình trạng chiếu, đặt lại trạng thái các ô được chọn
            self.reset_selected()

        # Cập nhật lại các nước đi hợp lệ sau khi di chuyển
        self.update_moves()
        # Nếu nước đi thực sự thay đổi, cập nhật thông tin về nước đi cuối cùng và thời gian lưu trữ
        if changed:
            self.last = [start, end]
            if self.turn == "w":
                self.storedTime1 += (time.time() - self.startTime)
            else:
                self.storedTime2 += (time.time() - self.startTime)
            self.startTime = time.time()

        return changed




