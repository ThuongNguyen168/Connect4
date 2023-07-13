import numpy as np
# sử dụng trong mảng, ma trận
import random
# tạo số ngẫu nhiên
import pygame
# tạo giao diện, âm thành game
import sys
# hứa các thông tin liên quan đến chính chương trình python interpreter đang chạy, cho phép thay đổi thông số
import math
# sqrt, pow

# Tạo ra bàn cờ màu trắng và đen
White = (255,255,255)
BLACK = (0,0,0)

# Tạo ra dòng chữ chiến thắng của AI hoặc con người 
Green = (255,255,0)
Pink = (255,0,255)

# Tạo dòng và số cột
Dong = 6
COLUMN_COUNT = 7

# Tạo thông số người chơi
PLAYER = 0
AI = 1
EMPTY = 0

# 
PLAYER_PIECE = 1 
AI_PIECE = 2
WINDOW_LENGTH = 4

# Tạo bàn cờ 6 dòng và 7 cột
def TaoBanCo():
	# tạo bảng bằng số 0
	ban = np.zeros((Dong,COLUMN_COUNT))
	return ban

def ThemVaoBanCo(ban, row, col, piece):
	ban[row][col] = piece

def kiemTraTrong(ban, col):
	return ban[Dong-1][col] == 0

def layGiaTriRow(ban, col):
	for r in range(Dong):
		if ban[r][col] == 0:
			return r
#dieu kien chien thang
def win(ban, piece):
	# chieu ngang
	for c in range(COLUMN_COUNT-3):
		for r in range(Dong):
			if ban[r][c] == piece and ban[r][c+1] == piece and ban[r][c+2] == piece and ban[r][c+3] == piece:
				return True

	# chieu doc
	for c in range(COLUMN_COUNT):
		for r in range(Dong-3):
			if ban[r][c] == piece and ban[r+1][c] == piece and ban[r+2][c] == piece and ban[r+3][c] == piece:
				return True

	# cheo phai
	for c in range(COLUMN_COUNT-3):
		for r in range(Dong-3):
			if ban[r][c] == piece and ban[r+1][c+1] == piece and ban[r+2][c+2] == piece and ban[r+3][c+3] == piece:
				return True

	# cheo trai
	for c in range(COLUMN_COUNT-3):
		for r in range(3, Dong):
			if ban[r][c] == piece and ban[r-1][c+1] == piece and ban[r-2][c+2] == piece and ban[r-3][c+3] == piece:
				return True


#tao kích thước window

def evaluate_window(window, piece):
	score = 0
	opp_piece = PLAYER_PIECE
	if piece == PLAYER_PIECE:
		opp_piece = AI_PIECE

	if window.count(piece) == 4:
		score += 100
	elif window.count(piece) == 3 and window.count(EMPTY) == 1:
		score += 5
	elif window.count(piece) == 2 and window.count(EMPTY) == 2:
		score += 2

	if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
		score -= 4

	return score

#xet diem chieu sau
def score_position(ban, piece):
	score = 0
	center_array = [int(i) for i in list(ban[:, COLUMN_COUNT//2])]
	center_count = center_array.count(piece)
	score += center_count * 3

	
	for r in range(Dong):
		row_array = [int(i) for i in list(ban[r,:])]
		for c in range(COLUMN_COUNT-3):
			window = row_array[c:c+WINDOW_LENGTH]
			score += evaluate_window(window, piece)


	for c in range(COLUMN_COUNT):
		col_array = [int(i) for i in list(ban[:,c])]
		for r in range(Dong-3):
			window = col_array[r:r+WINDOW_LENGTH]
			score += evaluate_window(window, piece)

	# đường chéo chính
	for r in range(Dong-3):
		for c in range(COLUMN_COUNT-3):
			window = [ban[r+i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, piece)
	# đường chéo phụ
	for r in range(Dong-3):
		for c in range(COLUMN_COUNT-3):
			window = [ban[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, piece)

	return score
def is_terminal_node(ban):
	return win(ban, PLAYER_PIECE) or win(ban, AI_PIECE) or len(get_valid_locations(ban)) == 0

def minimax(ban, depth, alpha, beta, maximizingPlayer):
	valid_locations = get_valid_locations(ban)
	is_terminal = is_terminal_node(ban)
	if depth == 0 or is_terminal:
		if is_terminal:
			if win(ban, AI_PIECE):
				return (None, 100000000000000)
			elif win(ban, PLAYER_PIECE):
				return (None, -10000000000000)
			else: # Game is over, no more valid moves
				return (None, 0)
		else: # Depth is zero
			return (None, score_position(ban, AI_PIECE))
	if maximizingPlayer:
		value = -math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = layGiaTriRow(ban, col)
			b_copy = ban.copy()
			ThemVaoBanCo(b_copy, row, col, AI_PIECE)
			new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
			if new_score > value:
				value = new_score
				column = col
			alpha = max(alpha, value)
			if alpha >= beta:
				break
		return column, value

	else: 
		value = math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = layGiaTriRow(ban, col)
			b_copy = ban.copy()
			ThemVaoBanCo(b_copy, row, col, PLAYER_PIECE)
			new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
			if new_score < value:
				value = new_score
				column = col
			beta = min(beta, value)
			if alpha >= beta:
				break
		return column, value

def get_valid_locations(ban):

	valid_locations = []
	for col in range(COLUMN_COUNT):
		if kiemTraTrong(ban, col):
			valid_locations.append(col)
	return valid_locations

# tao do hoa ban
def draw_ban(ban):
	for c in range(COLUMN_COUNT):
		for r in range(Dong):
			pygame.draw.rect(screen, White, (c*taokichthuoc, r*taokichthuoc+taokichthuoc, taokichthuoc, taokichthuoc))
			pygame.draw.circle(screen, BLACK, (int(c*taokichthuoc+taokichthuoc/2), int(r*taokichthuoc+taokichthuoc+taokichthuoc/2)), RADIUS)
	
	for c in range(COLUMN_COUNT):
		for r in range(Dong):		
			if ban[r][c] == PLAYER_PIECE:
				pygame.draw.circle(screen, Green, (int(c*taokichthuoc+taokichthuoc/2), height-int(r*taokichthuoc+taokichthuoc/2)), RADIUS)
			elif ban[r][c] == AI_PIECE: 
				pygame.draw.circle(screen, Pink, (int(c*taokichthuoc+taokichthuoc/2), height-int(r*taokichthuoc+taokichthuoc/2)), RADIUS)
	pygame.display.update()

ban = TaoBanCo()
game_over = False
pygame.init()


taokichthuoc = 100
width = COLUMN_COUNT * taokichthuoc
height = (Dong+1) * taokichthuoc
size = (width, height)
RADIUS = int(taokichthuoc/2 - 5)
screen = pygame.display.set_mode(size)
draw_ban(ban)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

turn = random.randint(PLAYER, AI)


# chay 
while not game_over:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

		if event.type == pygame.MOUSEMOTION:
			pygame.draw.rect(screen, BLACK, (0,0, width, taokichthuoc))
			posx = event.pos[0]
			if turn == PLAYER:
				pygame.draw.circle(screen, Green, (posx, int(taokichthuoc/2)), RADIUS)

		pygame.display.update()

		if event.type == pygame.MOUSEBUTTONDOWN:
			pygame.draw.rect(screen, BLACK, (0,0, width, taokichthuoc))
			
			if turn == PLAYER:
				posx = event.pos[0]
				col = int(math.floor(posx/taokichthuoc))

				if kiemTraTrong(ban, col):
					row = layGiaTriRow(ban, col)
					ThemVaoBanCo(ban, row, col, PLAYER_PIECE)

					if win(ban, PLAYER_PIECE):
						label = myfont.render("Player  wins!!", 1, Green)
						screen.blit(label, (20,10))
						game_over = True

					turn += 1
					turn = turn % 2
					draw_ban(ban)
	if turn == AI and not game_over:				
		col, minimax_score = minimax(ban, 5, -math.inf, math.inf, True)

		if kiemTraTrong(ban, col):
		
			row = layGiaTriRow(ban, col)
			ThemVaoBanCo(ban, row, col, AI_PIECE)

			if win(ban, AI_PIECE):
				label = myfont.render("AI win!!", 1, Pink)
				screen.blit(label, (40,10))
				game_over = True
			draw_ban(ban)

			turn += 1
			turn = turn % 2

	if game_over:
		pygame.time.wait(5000)