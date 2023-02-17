import pygame
import sys
import random
from pygame.math import Vector2


class SNAKE:
	def __init__(self):
		self.body = [Vector2(5, 15), Vector2(5, 16), Vector2(5, 17)]
		self.direction = Vector2(0, 0)

		self.head_up = pygame.image.load('img/head_up.png').convert_alpha()
		self.head_down = pygame.image.load('img/head_down.png').convert_alpha()
		self.head_right = pygame.image.load('img/head_right.png').convert_alpha()
		self.head_left = pygame.image.load('img/head_left.png').convert_alpha()

		self.tail_up = pygame.image.load('img/tail_up.png').convert_alpha()
		self.tail_down = pygame.image.load('img/tail_down.png').convert_alpha()
		self.tail_right = pygame.image.load('img/tail_right.png').convert_alpha()
		self.tail_left = pygame.image.load('img/tail_left.png').convert_alpha()

		self.body_vertical = pygame.image.load('img/body_vertical.png').convert_alpha()
		self.body_horizontal = pygame.image.load('img/body_horizontal.png').convert_alpha()
		self.body_vertical2 = pygame.image.load('img/body_vertical2.png').convert_alpha()
		self.body_horizontal2 = pygame.image.load('img/body_horizontal2.png').convert_alpha()

		self.body_tr = pygame.image.load('img/body_topright.png').convert_alpha()
		self.body_tl = pygame.image.load('img/body_topleft.png').convert_alpha()
		self.body_br = pygame.image.load('img/body_bottomright.png').convert_alpha()
		self.body_bl = pygame.image.load('img/body_bottomleft.png').convert_alpha()
		self.body_tr2 = pygame.image.load('img/body_topright2.png').convert_alpha()
		self.body_tl2 = pygame.image.load('img/body_topleft2.png').convert_alpha()
		self.body_br2 = pygame.image.load('img/body_bottomright2.png').convert_alpha()
		self.body_bl2 = pygame.image.load('img/body_bottomleft2.png').convert_alpha()

	def draw_snake(self):
		self.select_head()
		self.select_tail()

		for index, block in enumerate(self.body):
			x_pos = int(block.x * cell_size)
			y_pos = int(block.y * cell_size)
			block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

			if index == 0:
				game_window.blit(self.head, block_rect)
			elif index == len(self.body) - 1:
				game_window.blit(self.tail, block_rect)
			else:
				previous_block = self.body[index + 1] - block
				next_block = self.body[index - 1] - block
				# Condition for vertical move
				if previous_block.x == next_block.x:
					game_window.blit(self.body_vertical2, block_rect)
					if previous_block.y > next_block.y:
						game_window.blit(self.body_vertical, block_rect)
				# Condition for horizontal move
				elif previous_block.y == next_block.y:
					game_window.blit(self.body_horizontal, block_rect)
					if previous_block.x > next_block.x:
						game_window.blit(self.body_horizontal2, block_rect)
				# Condition for corners
				else:
					blit_images = {
						(-1, 0, 0, 1): self.body_bl,
						(0, -1, -1, 0): self.body_tl,
						(1, 0, 0, -1): self.body_tr,
						(0, 1, 1, 0): self.body_br,
						(-1, 0, 0, -1): self.body_tl2,
						(0, 1, -1, 0): self.body_bl2,
						(1, 0, 0, 1): self.body_br2,
						(0, -1, 1, 0): self.body_tr2,
					}
					direction = (
						int(previous_block.x),
						int(previous_block.y),
						int(next_block.x),
						int(next_block.y)
					)
					game_window.blit(blit_images[direction], block_rect)

	def select_head(self):
		direction_to_head = {
			(1, 0): self.head_left,
			(-1, 0): self.head_right,
			(0, 1): self.head_up,
			(0, -1): self.head_down
		}
		head_direction = tuple(self.body[1] - self.body[0])
		self.head = direction_to_head.get(head_direction)

	def select_tail(self):
		direction_to_tail = {
			(1, 0): self.tail_right,
			(-1, 0): self.tail_left,
			(0, 1): self.tail_down,
			(0, -1): self.tail_up
		}
		tail_direction = tuple(self.body[-2] - self.body[-1])
		self.tail = direction_to_tail.get(tail_direction)

	def move(self):
		body_copy = self.body[:-1]
		body_copy.insert(0, body_copy[0] + self.direction)
		self.body = body_copy[:]

	def add_block(self):
		body_copy = self.body[:]
		body_copy.insert(0, body_copy[0] + self.direction)
		self.body = body_copy[:]

	def reset(self):
		self.body = [Vector2(5, 15), Vector2(5, 16), Vector2(5, 17)]
		self.direction = Vector2(0, 0)



class FRUIT:
	def __init__(self):
		# Position of the fruit in a vector
		self.x = random.randint(0, cell_number_x - 1)
		self.y = random.randint(0, cell_number_y - 1)
		self.pos = Vector2(self.x, self.y)

		self.food = pygame.image.load('img/bird1.png').convert_alpha()

	def draw_fruit(self):
		# Draw a rectangle
		# Each position is a multiple of the size in order to create a grid effect
		fruit_rect = pygame.Rect(
			int(self.pos.x * cell_size),
			int(self.pos.y * cell_size),
			cell_size,
			cell_size)
		# pygame.draw.rect(game_window, (185, 76, 76), fruit_rect)
		game_window.blit(self.food, fruit_rect)


class MAIN:
	def __init__(self):
		self.snake = SNAKE()
		self.fruit = FRUIT()

	def update(self):
		self.snake.move()
		self.check_collision()
		self.check_fail()

	def draw(self):
		self.background()
		self.score()
		self.snake.draw_snake()
		self.fruit.draw_fruit()

	def check_collision(self):
		if self.fruit.pos == self.snake.body[0]:
			self.snake.add_block()
			self.fruit = FRUIT()

		for block in self.snake.body[1:]:
			if block == self.fruit.pos:
				self.fruit = FRUIT()

	def check_fail(self):
		if not (0 <= self.snake.body[0].x < cell_number_x) or \
			not (0 <= self.snake.body[0].y < cell_number_y):
			self.game_over()

		if Vector2(self.snake.body[0]) in self.snake.body[1:]:
			self.game_over()

	def game_over(self):
		self.snake.reset()

	def background(self):
		sky_color = (78, 192, 202)
		grass_color = (92, 226, 112)
		grass_color_2 = (167, 252, 179)

		for row in range(cell_number_y):
			if row % 2 == 0 and row <= cell_number_y / 2:
				for col in range(cell_number_x):
					if col % 2 == 0:
						sky_rect = pygame.Rect(
							col * cell_size,
							row * cell_size,
							cell_size,
							cell_size)
						pygame.draw.rect(game_window, sky_color, sky_rect)
			elif row % 2 != 0 and row <= cell_number_y / 2:
				for col in range(cell_number_x):
					if col % 2 != 0:
						sky_rect = pygame.Rect(
							col * cell_size,
							row * cell_size,
							cell_size,
							cell_size)
						pygame.draw.rect(game_window, sky_color, sky_rect)

			elif row % 2 == 0 and row > cell_number_y / 2:
				for col in range(cell_number_x):
					if col % 2 == 0:
						grass_rect = pygame.Rect(
							col * cell_size,
							row * cell_size,
							cell_size,
							cell_size)
						pygame.draw.rect(game_window, grass_color, grass_rect)
					else:
						grass_rect = pygame.Rect(
							col * cell_size,
							row * cell_size,
							cell_size,
							cell_size)
						pygame.draw.rect(game_window, grass_color_2, grass_rect)
			else:
				for col in range(cell_number_x):
					if col % 2 != 0:
						grass_rect = pygame.Rect(
							col * cell_size,
							row * cell_size,
							cell_size,
							cell_size)
						pygame.draw.rect(game_window, grass_color, grass_rect)
					else:
						grass_rect = pygame.Rect(
							col * cell_size,
							row * cell_size,
							cell_size,
							cell_size)
						pygame.draw.rect(game_window, grass_color_2, grass_rect)

	def score(self):
		score_val = str(len(self.snake.body) - 3)
		score_shown = font.render(score_val, True, (0, 0, 0))
		score_x = int(cell_size * cell_number_x - 60)
		score_y = int(cell_size * cell_number_y - 40)
		score_rect = score_shown.get_rect(center=(score_x, score_y))
		game_window.blit(score_shown, score_rect)


pygame.init()
# Variables
cell_size = 40
cell_number_x = 30
cell_number_y = 20
# Set window
game_window = pygame.display.set_mode((
	cell_size * cell_number_x,
	cell_size * cell_number_y))
# Clock speed
clock = pygame.time.Clock()
# Framerate
framerate = 60
font = pygame.font.SysFont('arialblack', 50)

GAME_UPDATE = pygame.USEREVENT
pygame.time.set_timer(GAME_UPDATE, 150)

main_game = MAIN()

while True:
	# Event loop, check every event
	for event in pygame.event.get():
		# if taype of event is clsoe game
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == GAME_UPDATE:
			main_game.update()

		if event.type == pygame.KEYDOWN:
			direction = main_game.snake.direction
			key_to_direction = {
				pygame.K_UP: Vector2(0, -1),
				pygame.K_DOWN: Vector2(0, 1),
				pygame.K_RIGHT: Vector2(1, 0),
				pygame.K_LEFT: Vector2(-1, 0)
			}
			new_direction = key_to_direction.get(event.key)

			if new_direction and new_direction != -direction:
				main_game.snake.direction = new_direction

	# Fill background with color
	game_window.fill((210, 240, 255))

	main_game.draw()

	# Redraw the window and its elements
	pygame.display.update()

	clock.tick(framerate)
