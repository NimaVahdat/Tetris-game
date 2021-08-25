import pygame
from pygame.locals import *
import random
point = 0

#Size
board_size = (6, 12)
tile_size = (20, 20)

#Color
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
pink = (255, 0, 128)
yellow = (255, 255, 0)
orange = (255, 128, 0)
purple = (128, 0, 128)
number = int(input('With how many color do you want to play(4 to 8)?\n'))

colors = [black, white, red, blue, green]
colors2 = [pink, yellow, orange, purple]

for i in range(number-4):
	colors.append(colors2[i])

pygame.init()
screen = pygame.display.set_mode((tile_size[0]*board_size[0], tile_size[1]*board_size[1]))

board = [None] * board_size[0]
for i in range(board_size[0]):
	board[i] = [black] * (board_size[1]+5)

#makeing a new action in the game
MOVE = pygame.USEREVENT + 1
inter = 1000
pygame.time.set_timer(MOVE, inter)

freez = None

c1 = colors[random.randint(1, len(colors)-1)]
c2 = colors[random.randint(1, len(colors)-1)]
q = [c1, c2]
remo = q[random.randint(0, len(q)-1)]
w = colors[:]
w.remove(remo)

c3 = colors[random.randint(1, len(w)-1)]
x = random.randint(0, board_size[0]-1)
y = 0
column_color = [c1, c2, c3]
for i in range(3):
	board[x][i] = column_color[i]

is_running = True
while is_running:
	direction = 0
	for event in pygame.event.get():
		if event.type == KEYDOWN:
			if event.key == K_q:
				is_running = False
			elif event.key == K_LEFT:
				if not freez:
					po = 0
					for j in range(3):
						if x-1 >= 0:
							if board[(x-1)%board_size[0]][y+j] == black:
								po += 1
							if po == 3:
								for i in range(3):
									board[(x-1)%board_size[0]][y+i] = board[x][y+i]
									board[x][y+i] = black
								x = (x - 1)%board_size[0]

			elif event.key == K_RIGHT:
				if not freez:
					po = 0
					for j in range(3):
						if x+1 < board_size[0]:
							if board[(x+1)%board_size[0]][y+j] == black:
								po += 1
							if po == 3:
								for i in range(3):
									board[(x+1)%board_size[0]][y+i] = board[x][y+i]
									board[x][y+i] = black
								x = (x + 1)%board_size[0]
			elif event.key == K_SPACE:
				if not freez:
					board[x][y], board[x][y+1] = board[x][y+1], board[x][y]
					board[x][y+1], board[x][y+2] = board[x][y+2], board[x][y+1]
				
		elif event.type == MOVE:
			if freez:
				i = 0
				c1 = colors[random.randint(1, len(colors)-1)]
				c2 = colors[random.randint(1, len(colors)-1)]
				q = [c1, c2]
				remo = q[random.randint(0, len(q)-1)]
				w = colors[:]
				w.remove(remo)
				c3 = colors[random.randint(1, len(w)-1)]
				column_color = [c1, c2, c3]
				x = random.randint(0, board_size[0]-1)
				while x in notx:
					x = random.randint(0, board_size[0]-1)
				y = 0
				for i in range(3):
					board[x][i] = column_color[i]
				freez = False
			if not freez:
				if y < 11:
					if board[x][y+3] == black:
						for i in range(3):
							board[x][y+3-i] = board[x][y-i+2]
						board[x][y] = black
						y += 1
					else:
						freez = True
				elif y == 11:
					for i in range(3):
						board[x][y+3-i] = board[x][y-i+2]
					board[x][y] = black
					freez = True


					
	if freez:
		b = []
		a = 0
		for j in range(board_size[1]+5):
			for i in range(board_size[0]):
				if b == [] or board[b[-1][0]][b[-1][1]] == board[i][j] and board[i][j] != black:
					if b == [] or b[-1][1] == j:
						a += 1
						b.append((i, j))
					else:
						a = 0
						b = []
				elif a >= 3:
					point += a
					for match in b:
						m, n = match
						board[m][n] = black
					b = []
					a = 0
				else:
					b = [(i, j)]
					a = 1
		b = []
		a = 0
		for i in range(board_size[0]):
			for j in range(board_size[1]+5-3, 2, -1):
				if b == [] or board[b[-1][0]][b[-1][1]] == board[i][j] and board[i][j] != black:
					if b == [] or b[-1][0] == i:
						a += 1
						b.append((i, j))
					else:
						a = 0
						b = []
				elif a >= 3:
					point += a
					for match in b:
						m, n = match
						board[m][n] = black
					b = []
					a = 0
				else:
					b = [(i, j)]
					a = 1
		for i in range(board_size[0]):
			for j in range(board_size[1]+5):
				a = 1
				b = [(i, j)]
				x = 1
				flag =True
				while flag:
					if i + x < board_size[0] and j + x < board_size[1]+5:
						if board[b[-1][0]][b[-1][1]] == board[i+x][j+x] and board[i+x][j+x] != black:
							b.append((i+x, j+x))
							a += 1
							x += 1
						elif a >= 3:
							point += a
							for match in b:
								m, n = match
								board[m][n] = black
							b = [(i+x, j+x)]
							a = 1
							x += 1
						else:
							b = [(i+x, j+x)]
							a = 1
							x += 1
					elif a >= 3:
						point += a
						for match in b:
							m, n = match
							board[m][n] = black
						b = [(i+x, j+x)]
						a = 1
						x += 1
						flag = False		
					else:
						flag = False

		for i in range(board_size[0]):
			for j in range(board_size[1]+5):
				a = 1
				b = [(i, j)]
				x = 1
				flag =True
				while flag:
					if i - x >= 0 and j + x < board_size[1]+5:
						if board[b[-1][0]][b[-1][1]] == board[i-x][j+x] and board[i-x][j+x] != black:
							b.append((i-x, j+x))
							a += 1
							x += 1
						elif a >= 3:
							point += a
							for match in b:
								m, n = match
								board[m][n] = black
							b = [(i-x, j+x)]
							a = 1
							x += 1
						else:
							b = [(i-x, j+x)]
							a = 1
							x += 1
					elif a >= 3:
						point += a
						for match in b:
							m, n = match
							board[m][n] = black
						b = [(i-x, j+x)]
						a = 1
						x += 1
						flag = False		
					else:
						flag = False						


		for i in range(board_size[0]):
			for j in range(board_size[1]+5-3, 3, -1):
				if board[i][j] == black and board[i][j-1] != black:
					board[i][j], board[i][j-1] = board[i][j-1], board[i][j] 

	for i in range(board_size[0]):
		for j in range(board_size[1]+5):
			pygame.draw.rect(screen, board[i][j], (i * tile_size[0], (j-3) * tile_size[1], tile_size[0]-2, tile_size[1]-2))
	pygame.display.flip()
	notx = []
	for i in range(board_size[0]):
		if board[i][3] != black and freez :
			notx.append(i)
	if len(notx) == board_size[0]:
		is_running == False		
		print('You loosed :(')							
print(point)