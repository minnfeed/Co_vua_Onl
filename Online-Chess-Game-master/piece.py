import pygame
import os

b_bishop = pygame.image.load(os.path.join("img", "black_bishop.png"))
b_king = pygame.image.load(os.path.join("img", "black_king.png"))
b_knight = pygame.image.load(os.path.join("img", "black_knight.png"))
b_pawn = pygame.image.load(os.path.join("img", "black_pawn.png"))
b_queen = pygame.image.load(os.path.join("img", "black_queen.png"))
b_rook = pygame.image.load(os.path.join("img", "black_rook.png"))

w_bishop = pygame.image.load(os.path.join("img", "white_bishop.png"))
w_king = pygame.image.load(os.path.join("img", "white_king.png"))
w_knight = pygame.image.load(os.path.join("img", "white_knight.png"))
w_pawn = pygame.image.load(os.path.join("img", "white_pawn.png"))
w_queen = pygame.image.load(os.path.join("img", "white_queen.png"))
w_rook = pygame.image.load(os.path.join("img", "white_rook.png"))

b = [b_bishop, b_king, b_knight, b_pawn, b_queen, b_rook]
w = [w_bishop, w_king, w_knight, w_pawn, w_queen, w_rook]

B = []
W = []

for img in b:
    B.append(pygame.transform.scale(img, (55, 55)))

for img in w:
    W.append(pygame.transform.scale(img, (55, 55)))


class Piece:
    img = -1
    rect = (113, 113, 525, 525)
    startX = rect[0]
    startY = rect[1]

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.selected = False
        self.move_list = []
        self.king = False
        self.pawn = False

    def isSelected(self):
        # Trả về trạng thái của thuộc tính selected của quân cờ
        return self.selected

    def update_valid_moves(self, board):
        # Cập nhật danh sách các nước đi hợp lệ cho quân cờ
        self.move_list = self.valid_moves(board)

    def draw(self, win, color):
        # Chọn hình ảnh đúng cho quân cờ tùy thuộc vào màu của quân cờ ("w" hoặc "b")
        if self.color == "w":
            drawThis = W[self.img]
        else:
            drawThis = B[self.img]

        # Tính toán tọa độ x và y cho vị trí vẽ của quân cờ trên cửa sổ trò chơi
        x = (4 - self.col) + round(self.startX + (self.col * self.rect[2] / 8))
        y = 3 + round(self.startY + (self.row * self.rect[3] / 8))

        # Nếu quân cờ đã được chọn và có màu của người chơi hiện tại, vẽ một đường viền màu đỏ xung quanh quân cờ
        if self.selected and self.color == color:
            pygame.draw.rect(win, (255, 0, 0), (x, y, 62, 62), 4)

        # Vẽ hình ảnh của quân cờ lên cửa sổ trò chơi
        win.blit(drawThis, (x, y))

    def change_pos(self, pos):
        # Thay đổi hàng và cột của quân cờ thành vị trí mới được chỉ định
        self.row = pos[0]
        self.col = pos[1]

    #trả về vị trí quân cờ
    def __str__(self):
        # Trả về một chuỗi biểu diễn cho vị trí của quân cờ, bao gồm hàng và cột
        return str(self.col) + " " + str(self.row)


def valid_moves(self, board):
    i = self.row  # Lấy hàng của quân cờ
    j = self.col  # Lấy cột của quân cờ

    moves = []  # Khởi tạo danh sách các nước đi hợp lệ

    # Di chuyển theo hướng TOP RIGHT
    djL = j + 1  # Bắt đầu từ ô bên phải của quân cờ
    djR = j - 1  # Bắt đầu từ ô bên trái của quân cờ
    for di in range(i - 1, -1, -1):  # Duyệt qua các hàng phía trên của quân cờ (từ hàng trên đến hàng dưới)
        if djL < 8:  # Kiểm tra xem vị trí di chuyển có trong bảng cờ không
            p = board[di][djL]
            if p == 0:  # Nếu ô trống, thêm vào danh sách nước đi hợp lệ
                moves.append((djL, di))
            elif p.color != self.color:  # Nếu có quân cờ của màu khác, thêm vào danh sách và dừng vòng lặp
                moves.append((djL, di))
                break
            else:  # Nếu có quân cờ cùng màu, dừng vòng lặp
                break
        else:  # Nếu vị trí di chuyển ra ngoài bảng cờ, dừng vòng lặp
            break
        djL += 1  # Tiếp tục di chuyển sang ô bên phải của hàng trên

    # Tương tự cho hướng TOP LEFT
    for di in range(i - 1, -1, -1):
        if djR > -1:  # Kiểm tra xem vị trí di chuyển có trong bảng cờ không
            p = board[di][djR]
            if p == 0:  # Nếu ô trống, thêm vào danh sách nước đi hợp lệ
                moves.append((djR, di))
            elif p.color != self.color:  # Nếu có quân cờ của màu khác, thêm vào danh sách và dừng vòng lặp
                moves.append((djR, di))
                break
            else:  # Nếu có quân cờ cùng màu, dừng vòng lặp
                break
        else:  # Nếu vị trí di chuyển ra ngoài bảng cờ, dừng vòng lặp
            break
        djR -= 1  # Tiếp tục di chuyển sang ô bên trái của hàng trên

    # Di chuyển theo hướng BOTTOM LEFT
    djL = j + 1  # Bắt đầu từ ô bên phải của quân cờ
    djR = j - 1  # Bắt đầu từ ô bên trái của quân cờ
    for di in range(i + 1, 8):  # Duyệt qua các hàng phía dưới của quân cờ (từ hàng dưới đến hàng trên)
        if djL < 8:  # Kiểm tra xem vị trí di chuyển có trong bảng cờ không
            p = board[di][djL]
            if p == 0:  # Nếu ô trống, thêm vào danh sách nước đi hợp lệ
                moves.append((djL, di))
            elif p.color != self.color:  # Nếu có quân cờ của màu khác, thêm vào danh sách và dừng vòng lặp
                moves.append((djL, di))
                break
            else:  # Nếu có quân cờ cùng màu, dừng vòng lặp
                break
        else:  # Nếu vị trí di chuyển ra ngoài bảng cờ, dừng vòng lặp
            break
        djL += 1  # Tiếp tục di chuyển sang ô bên phải của hàng dưới

    # Tương tự cho hướng BOTTOM RIGHT
    for di in range(i + 1, 8):
        if djR > -1:  # Kiểm tra xem vị trí di chuyển có trong bảng cờ không
            p = board[di][djR]
            if p == 0:  # Nếu ô trống, thêm vào danh sách nước đi hợp lệ
                moves.append((djR, di))
            elif p.color != self.color:  # Nếu có quân cờ của màu khác, thêm vào danh sách và dừng vòng lặp
                moves.append((djR, di))
                break
            else:  # Nếu có quân cờ cùng màu, dừng vòng lặp
                break
        else:  # Nếu vị trí di chuyển ra ngoài bảng cờ, dừng vòng lặp
            break
        djR -= 1  # Tiếp tục di chuyển sang ô bên trái của hàng dưới

    return moves  # Trả về danh sách các nước đi hợp lệ cho quân Tượng


class King(Piece):
    img = 1

    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.king = True

    def valid_moves(self, board):
        i = self.row  # Lấy hàng của vua
        j = self.col  # Lấy cột của vua

        moves = []  # Khởi tạo danh sách các nước đi hợp lệ

        if i > 0:
            # TOP LEFT (Đi lên trái)
            if j > 0:  # Kiểm tra xem có thể đi lên trái không
                p = board[i - 1][j - 1]  # Kiểm tra ô bên trái phía trên
                if p == 0:  # Nếu ô trống, thêm vào danh sách nước đi hợp lệ
                    moves.append((j - 1, i - 1,))
                elif p.color != self.color:  # Nếu có quân cờ của màu đối phương, thêm vào danh sách nước đi hợp lệ
                    moves.append((j - 1, i - 1,))

            # TOP MIDDLE (Đi lên trên)
            p = board[i - 1][j]  # Kiểm tra ô phía trên
            if p == 0:  # Nếu ô trống, thêm vào danh sách nước đi hợp lệ
                moves.append((j, i - 1))
            elif p.color != self.color:  # Nếu có quân cờ của màu đối phương, thêm vào danh sách nước đi hợp lệ
                moves.append((j, i - 1))

            # TOP RIGHT (Đi lên phải)
            if j < 7:  # Kiểm tra xem có thể đi lên phải không
                p = board[i - 1][j + 1]  # Kiểm tra ô bên phải phía trên
                if p == 0:  # Nếu ô trống, thêm vào danh sách nước đi hợp lệ
                    moves.append((j + 1, i - 1,))
                elif p.color != self.color:  # Nếu có quân cờ của màu đối phương, thêm vào danh sách nước đi hợp lệ
                    moves.append((j + 1, i - 1,))

        if i < 7:
            # BOTTOM LEFT (Đi xuống trái)
            if j > 0:  # Kiểm tra xem có thể đi xuống trái không
                p = board[i + 1][j - 1]  # Kiểm tra ô bên trái phía dưới
                if p == 0:  # Nếu ô trống, thêm vào danh sách nước đi hợp lệ
                    moves.append((j - 1, i + 1,))
                elif p.color != self.color:  # Nếu có quân cờ của màu đối phương, thêm vào danh sách nước đi hợp lệ
                    moves.append((j - 1, i + 1,))

            # BOTTOM MIDDLE (Đi xuống dưới)
            p = board[i + 1][j]  # Kiểm tra ô phía dưới
            if p == 0:  # Nếu ô trống, thêm vào danh sách nước đi hợp lệ
                moves.append((j, i + 1))
            elif p.color != self.color:  # Nếu có quân cờ của màu đối phương, thêm vào danh sách nước đi hợp lệ
                moves.append((j, i + 1))

            # BOTTOM RIGHT (Đi xuống phải)
            if j < 7:  # Kiểm tra xem có thể đi xuống phải không
                p = board[i + 1][j + 1]  # Kiểm tra ô bên phải phía dưới
                if p == 0:  # Nếu ô trống, thêm vào danh sách nước đi hợp lệ
                    moves.append((j + 1, i + 1))
                elif p.color != self.color:  # Nếu có quân cờ của màu đối phương, thêm vào danh sách nước đi hợp lệ
                    moves.append((j + 1, i + 1))

        # MIDDLE LEFT (Đi sang trái)
        if j > 0:  # Kiểm tra xem có thể đi sang trái không
            p = board[i][j - 1]  # Kiểm tra ô bên trái
            if p == 0:  # Nếu ô trống, thêm vào danh sách nước đi hợp lệ
                moves.append((j - 1, i))
            elif p.color != self.color:  # Nếu có quân cờ của màu đối phương, thêm vào danh sách nước đi hợp lệ
                moves.append((j - 1, i))

        # MIDDLE RIGHT (Đi sang phải)
        if j < 7:  # Kiểm tra xem có thể đi sang phải không
            p = board[i][j + 1]  # Kiểm tra ô bên phải
            if p == 0:  # Nếu ô trống, thêm vào danh sách nước đi hợp lệ
                moves.append((j + 1, i))

        return moves


class Knight(Piece):
    img = 2  # Định danh hình ảnh cho quân mã

    def valid_moves(self, board):
        i = self.row  # Lấy chỉ số hàng của quân mã
        j = self.col  # Lấy chỉ số cột của quân mã

        moves = []  # Khởi tạo danh sách các nước đi hợp lệ cho quân mã

        # Xuống bên trái
        if i < 6 and j > 0:  # Kiểm tra xem có thể đi xuống và sang trái không
            p = board[i + 2][j - 1]  # Kiểm tra ô phía dưới và bên trái
            if p == 0:  # Nếu ô trống, thêm vào danh sách các nước đi hợp lệ
                moves.append((j - 1, i + 2))
            elif p.color != self.color:  # Nếu có quân đối phương, thêm vào danh sách các nước đi hợp lệ
                moves.append((j - 1, i + 2))

        # Lên bên trái
        if i > 1 and j > 0:  # Kiểm tra xem có thể đi lên và sang trái không
            p = board[i - 2][j - 1]  # Kiểm tra ô phía trên và bên trái
            if p == 0:  # Nếu ô trống, thêm vào danh sách các nước đi hợp lệ
                moves.append((j - 1, i - 2))
            elif p.color != self.color:  # Nếu có quân đối phương, thêm vào danh sách các nước đi hợp lệ
                moves.append((j - 1, i - 2))

        # Xuống bên phải
        if i < 6 and j < 7:  # Kiểm tra xem có thể đi xuống và sang phải không
            p = board[i + 2][j + 1]  # Kiểm tra ô phía dưới và bên phải
            if p == 0:  # Nếu ô trống, thêm vào danh sách các nước đi hợp lệ
                moves.append((j + 1, i + 2))
            elif p.color != self.color:  # Nếu có quân đối phương, thêm vào danh sách các nước đi hợp lệ
                moves.append((j + 1, i + 2))

        # Lên bên phải
        if i > 1 and j < 7:  # Kiểm tra xem có thể đi lên và sang phải không
            p = board[i - 2][j + 1]  # Kiểm tra ô phía trên và bên phải
            if p == 0:  # Nếu ô trống, thêm vào danh sách các nước đi hợp lệ
                moves.append((j + 1, i - 2))
            elif p.color != self.color:  # Nếu có quân đối phương, thêm vào danh sách các nước đi hợp lệ
                moves.append((j + 1, i - 2))

        if i > 0 and j > 1:  # Kiểm tra xem có thể đi lên và sang trái hai ô không
            p = board[i - 1][j - 2]  # Kiểm tra ô phía trên và bên trái hai ô
            if p == 0:  # Nếu ô trống, thêm vào danh sách các nước đi hợp lệ
                moves.append((j - 2, i - 1))
            elif p.color != self.color:  # Nếu có quân đối phương, thêm vào danh sách các nước đi hợp lệ
                moves.append((j - 2, i - 1))

        if i > 0 and j < 6:  # Kiểm tra xem có thể đi lên và sang phải hai ô không
            p = board[i - 1][j + 2]  # Kiểm tra ô phía trên và bên phải hai ô
            if p == 0:  # Nếu ô trống, thêm vào danh sách các nước đi hợp lệ
                moves.append((j + 2, i - 1))
            elif p.color != self.color:  # Nếu có quân đối phương, thêm vào danh sách các nước đi hợp lệ
                moves.append((j + 2, i - 1))

        if i < 7 and j > 1:  # Kiểm tra xem có thể đi xuống và sang trái hai ô không
            p = board[i + 1][j - 2]  # Kiểm tra ô phía dưới và bên trái hai ô
            if p == 0:  # Nếu ô trống, thêm vào danh sách các nước đi hợp lệ
                moves.append((j - 2, i + 1))
            elif p.color != self.color:  # Nếu có quân đối phương, thêm vào danh sách các nước đi hợp lệ
                moves.append((j - 2, i + 1))

        if i < 7 and j < 6:  # Kiểm tra xem có thể đi xuống và sang phải hai ô không
            p = board[i + 1][j + 2]  # Kiểm tra ô phía dưới và bên phải hai ô
            if p == 0:  # Nếu ô trống, thêm vào danh sách các nước đi hợp lệ
                moves.append((j + 2, i + 1))
            elif p.color != self.color:  # Nếu có quân đối phương, thêm vào danh sách các nước đi hợp lệ
                moves.append((j + 2, i + 1))

        return moves  # Trả về danh sách các nước đi hợp lệ cho quân mã



class Pawn(Piece):
    img = 3  # Định danh hình ảnh cho quân tốt

    def __init__(self, row, col, color):
        super().__init__(row, col, color)  # Gọi hàm khởi tạo của lớp cha với hàng, cột, và màu sắc
        self.first = True  # Đánh dấu xem quân tốt đã di chuyển lần đầu tiên hay chưa
        self.queen = False  # Đánh dấu xem quân tốt có được thăng hậu hay không
        self.pawn = True  # Đánh dấu xem đây có phải là quân tốt không

    def valid_moves(self, board):
        i = self.row  # Lấy chỉ số hàng của quân tốt
        j = self.col  # Lấy chỉ số cột của quân tốt

        moves = []  # Khởi tạo danh sách các nước đi hợp lệ cho quân tốt

        try:
            if self.color == "b":  # Nếu là quân tốt màu đen
                if i < 7:  # Nếu quân tốt chưa đến hàng cuối cùng của bàn cờ
                    p = board[i + 1][j]  # Kiểm tra ô phía dưới
                    if p == 0:  # Nếu ô trống, thêm vào danh sách các nước đi hợp lệ
                        moves.append((j, i + 1))

                    # DIAGONAL
                    if j < 7:  # Nếu không ở cột cuối cùng
                        p = board[i + 1][j + 1]  # Kiểm tra ô chéo phải dưới
                        if p != 0:  # Nếu ô không trống
                            if p.color != self.color:  # Nếu có quân đối phương
                                moves.append((j + 1, i + 1))  # Thêm vào danh sách nước đi hợp lệ

                    if j > 0:  # Nếu không ở cột đầu tiên
                        p = board[i + 1][j - 1]  # Kiểm tra ô chéo trái dưới
                        if p != 0:  # Nếu ô không trống
                            if p.color != self.color:  # Nếu có quân đối phương
                                moves.append((j - 1, i + 1))  # Thêm vào danh sách nước đi hợp lệ

                if self.first:  # Nếu là lần di chuyển đầu tiên của quân tốt
                    if i < 6:  # Nếu quân tốt có thể di chuyển hai ô về phía trước
                        p = board[i + 2][j]  # Kiểm tra ô hai ô phía dưới
                        if p == 0:  # Nếu ô trống
                            if board[i + 1][j] == 0:  # Nếu ô ngay phía dưới cũng trống
                                moves.append((j, i + 2))  # Thêm vào danh sách nước đi hợp lệ
                        elif p.color != self.color:  # Nếu có quân đối phương
                            moves.append((j, i + 2))  # Thêm vào danh sách nước đi hợp lệ

            # WHITE
            else:  # Nếu là quân tốt màu trắng
                if i > 0:  # Nếu quân tốt chưa đến hàng cuối cùng của bàn cờ
                    p = board[i - 1][j]  # Kiểm tra ô phía trên
                    if p == 0:  # Nếu ô trống, thêm vào danh sách các nước đi hợp lệ
                        moves.append((j, i - 1))

                if j < 7:  # Nếu không ở cột cuối cùng
                    p = board[i - 1][j + 1]  # Kiểm tra ô chéo phải trên
                    if p != 0:  # Nếu ô không trống
                        if p.color != self.color:  # Nếu có quân đối phương
                            moves.append((j + 1, i - 1))  # Thêm vào danh sách nước đi hợp lệ

                if j > 0:  # Nếu không ở cột đầu tiên
                    p = board[i - 1][j - 1]  # Kiểm tra ô chéo trái trên
                    if p != 0:  # Nếu ô không trống
                        if p.color != self.color:  # Nếu có quân đối phương
                            moves.append((j - 1, i - 1))  # Thêm vào danh sách nước đi hợp lệ

                if self.first:  # Nếu là lần di chuyển đầu tiên của quân tốt
                    if i > 1:  # Nếu quân tốt có thể di chuyển hai ô về phía trước
                        p = board[i - 2][j]  # Kiểm tra ô hai ô phía trên
                        if p == 0:  # Nếu ô trống
                            if board[i - 1][j] == 0:  # Nếu ô ngay phía trên cũng trống
                                moves.append((j, i - 2))  # Thêm vào danh sách nước đi hợp lệ
                        elif p.color != self.color:  # Nếu có quân đối phương
                            moves.append((j, i - 2))  # Thêm vào danh sách nước đi hợp lệ

        except:  # Bắt ngoại lệ để tránh lỗi nếu chỉ số hàng hoặc cột vượt quá kích thước của bảng
            pass

        return moves  # Trả về danh sách các nước đi hợp lệ cho quân tốt

class Queen(Piece):
    img = 4  # Định danh hình ảnh cho quân hậu

    def valid_moves(self, board):
        i = self.row  # Lấy chỉ số hàng của quân hậu
        j = self.col  # Lấy chỉ số cột của quân hậu

        moves = []  # Khởi tạo danh sách các nước đi hợp lệ cho quân hậu

        # Di chuyển theo đường chéo trên bên phải (TOP RIGHT)
        djL = j + 1
        djR = j - 1
        for di in range(i - 1, -1, -1):  # Duyệt qua các hàng phía trên từ hàng hiện tại
            if djL < 8:  # Nếu không vượt ra khỏi bàn cờ
                p = board[di][djL]  # Kiểm tra ô trên bên phải
                if p == 0:  # Nếu ô trống
                    moves.append((djL, di))  # Thêm vào danh sách các nước đi hợp lệ
                elif p.color != self.color:  # Nếu có quân đối phương
                    moves.append((djL, di))  # Thêm vào danh sách các nước đi hợp lệ
                    break  # Dừng lại vì đã gặp quân đối phương
                else:  # Nếu gặp quân của mình
                    djL = 9  # Đánh dấu để dừng vòng lặp
            djL += 1  # Di chuyển sang ô tiếp theo bên phải

        for di in range(i - 1, -1, -1):  # Duyệt qua các hàng phía trên từ hàng hiện tại
            if djR > -1:  # Nếu không vượt ra khỏi bàn cờ
                p = board[di][djR]  # Kiểm tra ô trên bên trái
                if p == 0:  # Nếu ô trống
                    moves.append((djR, di))  # Thêm vào danh sách các nước đi hợp lệ
                elif p.color != self.color:  # Nếu có quân đối phương
                    moves.append((djR, di))  # Thêm vào danh sách các nước đi hợp lệ
                    break  # Dừng lại vì đã gặp quân đối phương
                else:  # Nếu gặp quân của mình
                    djR = -1  # Đánh dấu để dừng vòng lặp
            djR -= 1  # Di chuyển sang ô tiếp theo bên trái

        # Di chuyển theo đường chéo dưới bên trái (TOP LEFT)
        djL = j + 1
        djR = j - 1
        for di in range(i + 1, 8):  # Duyệt qua các hàng phía dưới từ hàng hiện tại
            if djL < 8:  # Nếu không vượt ra khỏi bàn cờ
                p = board[di][djL]  # Kiểm tra ô dưới bên phải
                if p == 0:  # Nếu ô trống
                    moves.append((djL, di))  # Thêm vào danh sách các nước đi hợp lệ
                elif p.color != self.color:  # Nếu có quân đối phương
                    moves.append((djL, di))  # Thêm vào danh sách các nước đi hợp lệ
                    break  # Dừng lại vì đã gặp quân đối phương
                else:  # Nếu gặp quân của mình
                    djL = 9  # Đánh dấu để dừng vòng lặp
            djL += 1  # Di chuyển sang ô tiếp theo bên phải

            if djR > -1:  # Nếu không vượt ra khỏi bàn cờ
                p = board[di][djR]  # Kiểm tra ô dưới bên trái
                if p == 0:  # Nếu ô trống
                    moves.append((djR, di))  # Thêm vào danh sách các nước đi hợp lệ
                elif p.color != self.color:  # Nếu có quân đối phương
                    moves.append((djR, di))  # Thêm vào danh sách các nước đi hợp lệ
                    break  # Dừng lại vì đã gặp quân đối phương
                else:  # Nếu gặp quân của mình
                    djR = -1  # Đánh dấu để dừng vòng lặp
            djR -= 1  # Di chuyển sang ô tiếp theo bên trái

        # Di chuyển theo hướng lên (UP)
        for x in range(i - 1, -1, -1):  # Duyệt qua các hàng phía trên từ hàng hiện tại
            p = board[x][j]  # Kiểm tra ô phía trên
            if p == 0:  # Nếu ô trống
                moves.append((j, x))  # Thêm vào danh sách các nước đi hợp lệ
            elif p.color != self.color:  # Nếu có quân đối phương
                moves.append((j, x))  # Thêm vào danh sách các nước đi hợp lệ
                break  # Dừng lại vì đã gặp quân đối phương
            else:  # Nếu gặp quân của mình
                break  # Dừng lại vì đã gặp quân của mình

        # Di chuyển theo hướng xuống (DOWN)
        for x in range(i + 1, 8, 1):  # Duyệt qua các hàng phía dưới từ hàng hiện tại
            p = board[x][j]  # Kiểm tra ô phía dưới
            if p == 0:  # Nếu ô trống
                moves.append((j, x))  # Thêm vào danh sách các nước đi hợp lệ
            elif p.color != self.color:  # Nếu có quân đối phương
                moves.append((j, x))  # Thêm vào danh sách các nước đi hợp lệ
                break  # Dừng lại vì đã gặp quân đối phương
            else:  # Nếu gặp quân của mình
                break  # Dừng lại vì đã gặp quân của mình

        # Di chuyển theo hướng sang trái (LEFT)
        for x in range(j - 1, -1, -1):  # Duyệt qua các cột bên trái từ cột hiện tại
            p = board[i][x]  # Kiểm tra ô bên trái
            if p == 0:  # Nếu ô trống
                moves.append((x, i))  # Thêm vào danh sách các nước đi hợp lệ
            elif p.color != self.color:  # Nếu có quân đối phương
                moves.append((x, i))  # Thêm vào danh sách các nước đi hợp lệ
                break  # Dừng lại vì đã gặp quân đối phương
            else:  # Nếu gặp quân của mình
                break  # Dừng lại vì đã gặp quân của mình

        # Di chuyển theo hướng sang phải (RIGHT)
        for x in range(j + 1, 8, 1):  # Duyệt qua các cột bên phải từ cột hiện tại
            p = board[i][x]  # Kiểm tra ô bên phải
            if p == 0:  # Nếu ô trống
                moves.append((x, i))  # Thêm vào danh sách các nước đi hợp lệ
            elif p.color != self.color:  # Nếu có quân đối phương
                moves.append((x, i))  # Thêm vào danh sách các nước đi hợp lệ
                break  # Dừng lại vì đã gặp quân đối phương
            else:  # Nếu gặp quân của mình
                break  # Dừng lại vì đã gặp quân của mình

        return moves  # Trả về danh sách các nước đi hợp lệ cho quân hậu


class Rook(Piece):
    img = 5  # Định danh hình ảnh cho quân xe

    def valid_moves(self, board):
        i = self.row  # Lấy chỉ số hàng của quân xe
        j = self.col  # Lấy chỉ số cột của quân xe

        moves = []  # Khởi tạo danh sách các nước đi hợp lệ cho quân xe

        # Di chuyển theo hướng lên (UP)
        for x in range(i - 1, -1, -1):  # Duyệt qua các hàng phía trên từ hàng hiện tại
            p = board[x][j]  # Kiểm tra ô phía trên
            if p == 0:  # Nếu ô trống
                moves.append((j, x))  # Thêm vào danh sách các nước đi hợp lệ
            elif p.color != self.color:  # Nếu có quân đối phương
                moves.append((j, x))  # Thêm vào danh sách các nước đi hợp lệ
                break  # Dừng lại vì đã gặp quân đối phương
            else:  # Nếu gặp quân của mình
                break  # Dừng lại vì đã gặp quân của mình

        # Di chuyển theo hướng xuống (DOWN)
        for x in range(i + 1, 8, 1):  # Duyệt qua các hàng phía dưới từ hàng hiện tại
            p = board[x][j]  # Kiểm tra ô phía dưới
            if p == 0:  # Nếu ô trống
                moves.append((j, x))  # Thêm vào danh sách các nước đi hợp lệ
            elif p.color != self.color:  # Nếu có quân đối phương
                moves.append((j, x))  # Thêm vào danh sách các nước đi hợp lệ
                break  # Dừng lại vì đã gặp quân đối phương
            else:  # Nếu gặp quân của mình
                break  # Dừng lại vì đã gặp quân của mình

        # Di chuyển theo hướng sang trái (LEFT)
        for x in range(j - 1, -1, -1):  # Duyệt qua các cột bên trái từ cột hiện tại
            p = board[i][x]  # Kiểm tra ô bên trái
            if p == 0:  # Nếu ô trống
                moves.append((x, i))  # Thêm vào danh sách các nước đi hợp lệ
            elif p.color != self.color:  # Nếu có quân đối phương
                moves.append((x, i))  # Thêm vào danh sách các nước đi hợp lệ
                break  # Dừng lại vì đã gặp quân đối phương
            else:  # Nếu gặp quân của mình
                break  # Dừng lại vì đã gặp quân của mình

        # Di chuyển theo hướng sang phải (RIGHT)
        for x in range(j + 1, 8, 1):  # Duyệt qua các cột bên phải từ cột hiện tại
            p = board[i][x]  # Kiểm tra ô bên phải
            if p == 0:  # Nếu ô trống
                moves.append((x, i))  # Thêm vào danh sách các nước đi hợp lệ
            elif p.color != self.color:  # Nếu có quân đối phương
                moves.append((x, i))  # Thêm vào danh sách các nước đi hợp lệ
                break  # Dừng lại vì đã gặp quân đối phương
            else:  # Nếu gặp quân của mình
                break  # Dừng lại vì đã gặp quân của mình

        return moves  # Trả về danh sách các nước đi hợp lệ cho quân xe

