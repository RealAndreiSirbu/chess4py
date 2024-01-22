import pygame

window = pygame.display.set_mode((784, 784))
pygame.display.set_caption("chess4py")
board_img = pygame.image.load('rect-8x8.png')
selected_sqr_img = pygame.image.load('selected-square.png')
available_sqr_img = pygame.image.load('available-square.png')
sqr_size = {'x': 96, 'y': 96}
border_width = 8
border_height = border_width

class Piece:
	def __init__(self, y, x, piece_type, color):
		self.y = y
		self.x = x
		self.type = piece_type
		self.color = color
		self.selected = False
		self.sqr = pygame.Rect(self.x * sqr_size['x'] + border_width, self.y * sqr_size['y'] + border_height, sqr_size['x'], sqr_size['y'])

		self.img = pygame.image.load(f'{color}-{piece_type}.png')
		self.img = pygame.transform.scale(self.img, (sqr_size['x'], sqr_size['y']))

	def draw(self, board):
		if self.selected:
			window.blit(selected_sqr_img, (self.x * sqr_size['x'] + border_width, self.y * sqr_size['y'] + border_height))

			moves = self.available_moves(board)

			for move in moves:
				window.blit(available_sqr_img, (move[1] * sqr_size['x'] + border_width, move[0] * sqr_size['y'] + border_height))

		window.blit(self.img, (self.x * sqr_size['x'] + border_width, self.y * sqr_size['y'] + border_height))

	def update(self, event, board):
		self.sqr = pygame.Rect(self.x * sqr_size['x'] + border_width, self.y * sqr_size['y'] + border_height, sqr_size['x'], sqr_size['y'])
		moves = self.available_moves(board)

		if event == None:
			return

		if event.type == pygame.MOUSEBUTTONDOWN:
			if self.sqr.collidepoint(pygame.mouse.get_pos()):
				self.selected = not self.selected
			elif self.selected:
				for move in moves:
					sqr = pygame.Rect(move[1] * sqr_size['x'] + border_width, move[0] * sqr_size['y'] + border_height, sqr_size['x'], sqr_size['y'])

					if sqr.collidepoint(pygame.mouse.get_pos()):
						tmp = board[self.y][self.x]
						board[self.y][self.x] = None
						self.y = move[0]
						self.x = move[1]
						board[self.y][self.x] = tmp
					self.selected = False


	# Returns the available moves a piece can do in the form [(y, x)]
	def available_moves(self, board):
		return []

class Rook(Piece):
	def available_moves(self, board):
		moves = []

		for y in range(self.y + 1, 8):
			if board[y][self.x] == None:
				moves.append((y, self.x))
			else:
				break

		for y in range(self.y - 1, -1, -1):
			if board[y][self.x] == None:
				moves.append((y, self.x))
			else:
				break

		for x in range(self.x + 1, 8):
			if board[self.y][x] == None:
				moves.append((self.y, x))
			else:
				break

		for x in range(self.x - 1, -1, -1):
			if board[self.y][x] == None:
				moves.append((self.y, x))
			else:
				break

		return moves

pieces = [
	Rook(0, 0, 'rook', 'black'),
	Rook(0, 7, 'rook', 'black'),
	Rook(7, 0, 'rook', 'white'),
	Rook(7, 7, 'rook', 'white')
]
board = []

for y in range(0, 8):
	board.append([])
	for x in range(0, 8):
		board[y].append(None)

for piece in pieces:
	board[piece.y][piece.x] = piece

running = True
while running:
	event = None
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	window.blit(board_img, (0, 0))

	for piece in pieces:
		piece.draw(board)

	for piece in pieces:
		piece.update(event, board)

	pygame.display.update()

pygame.quit()