# Set Game - this is a limited version of a 1 player SET game, this game only support a table of 4 rows.
# 
# Alex Mak

import pygame
import sys
import Card
import random
import Board

pygame.init()

Deck = []
DeckIndex = 0
SetCount = 0
PossibleMatches = 0

# Screen
WIDTH = 750
ROWS = 4
win = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("SET Game - Alex Mak")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

SCORE_FONT = pygame.font.SysFont("Comic Sans MS", 20)
END_FONT = pygame.font.SysFont('courier', 40)

# Images
image_w = 170
image_h = 100

b = None
PNGS = []

def load_images():

	for i in range(0,82):
		filename = "images/slide" + str(i) + ".png"
		PNG = pygame.transform.scale(pygame.image.load(filename), (image_w, image_h))
		PNGS.append(PNG)


def draw_grid():
	gap = WIDTH // ROWS

	x = 0
	for i in range(ROWS):
		x = i * gap

		pygame.draw.line(win, GRAY, (x, 0), (x, WIDTH), 3)
		pygame.draw.line(win, GRAY, (0, x), (WIDTH, x), 3)

def card_image(index):
	if ( b.CardList[index].nth == -1):
		png = PNGS[0]
	else:
		png = PNGS[b.CardList[index].nth]

	return png	


def distribute_cards():
	global b
	box_size = WIDTH / 4
	offset = 8
	col = image_w // 2 + offset
	
	i = 0
	for r in range(0, b.Rows):		
		row = r * box_size + image_h - offset
		for c in range(0, 4):
			if b.Rows == 4:
				images.append((c * box_size + col,row, PNGS[0]))
			else:
				images.append((c * box_size + col,row, card_image(i)))
				i+= 1

	#print(f"there are {b.Rows} rows")
	#b.PrintCardList()

def initialize_board():
	global b
	global PossibleMatches
	
	i = 1 # start with 1, blank is not in the Deck
	for s in range(1,4):
		for c in range(1,4):
			for n in range(1,4):
				for f in range(1,4):
					card = Card.Card(s, c, n, f, i)
					Deck.append(card)
					i += 1

	random.shuffle(Deck)

	b = Board.Board(Deck)
	#b.PrintDeck()

	PossibleMatches = b.CheckSetsIndex()
	if PossibleMatches == 0:
		print("Whoa unusual, need 4th row")
		b.AddRow()
		PossibleMatches = b.CheckSetsIndex()
		if PossibleMatches == 0:
			game_over()
			return False

	load_images()
	distribute_cards()
	return True
	
	
boxes_clicked = []

def click():
	global images
	global click_count
	global b
	global SetCount
	global PossibleMatches

	# Mouse position
	m_x, m_y = pygame.mouse.get_pos()
	box_size = 186
	box_clicked = -1

	if m_y < box_size:
		if m_x < box_size:
			box_clicked = 0
		elif m_x > 1 * box_size and m_x < 2 * box_size:
			box_clicked = 1
		elif m_x > 2 * box_size and m_x < 3 * box_size:
			box_clicked = 2
		elif m_x > 3 * box_size and m_x < 4 * box_size:
			box_clicked = 3
	elif m_y > box_size and m_y < 2* box_size:
		if m_x < box_size:
			box_clicked = 4
		elif m_x > 1 * box_size and m_x < 2 * box_size:
			box_clicked = 5
		elif m_x > 2 * box_size and m_x < 3 * box_size:
			box_clicked = 6
		elif m_x > 3 * box_size and m_x < 4 * box_size:
			box_clicked = 7
	elif m_y > 2* box_size and m_y <  3* box_size:
		if m_x < box_size:
			box_clicked = 8
		elif m_x > 1 * box_size and m_x < 2* box_size:
			box_clicked = 9
		elif m_x > 2 * box_size and m_x < 3 * box_size:
			box_clicked = 10
		elif m_x > 3 * box_size and m_x < 4 * box_size:
			box_clicked = 11
	elif m_y > 3* box_size and m_y < 4* box_size:
		if m_x < box_size:
			box_clicked = 12
		elif m_x > 1 * box_size and m_x < 2 * box_size:
			box_clicked = 13
		elif m_x > 2 * box_size and m_x < 3 * box_size:
			box_clicked = 14
		elif m_x > 3 * box_size and m_x < 4 * box_size:
			box_clicked = 15

	#print(f"box clicked {box_clicked}")

	if box_clicked not in boxes_clicked:
		boxes_clicked.append(box_clicked)

	if (len(boxes_clicked) == 3):
		#print("got 3 boxes")
		#print(boxes_clicked)
		if b.IsSet(boxes_clicked) == True:
			print("got a set!")
			SetCount += 1
			b.ReplaceCardsByIndex(boxes_clicked)
			#b.PrintDeck()

			PossibleMatches = b.CheckSetsIndex()

			distribute_cards()
			if b.DeckIndex >= 81:
				game_over("Game Over")
				return False

		boxes_clicked.clear()
	return True

def game_over(content):
    pygame.time.delay(500)
    win.fill(WHITE)
    end_text = END_FONT.render(content, 1, BLACK)
    win.blit(end_text, ((WIDTH - end_text.get_width()) // 2, (WIDTH - end_text.get_height()) // 2))
    pygame.display.update()
    pygame.time.delay(5000)

def display_score():

	global SetCount
	global PossibleMatches

	message = ""
	if (SetCount == 1):
		message = "Score: " + str(SetCount) + " set"
	elif (SetCount > 1):
		message = "Score " + str(SetCount) + " sets"
	
	text_surface = SCORE_FONT.render(message, False, BLACK)
	win.blit(text_surface, (10,10))

	possible_text = ""
	if (PossibleMatches == 1):
		possible_text = str(PossibleMatches) + " set possible"
	elif (PossibleMatches > 1):
		possible_text = str(PossibleMatches) + " sets possible"

	possible_surface = SCORE_FONT.render(possible_text, False, BLACK)
	win.blit(possible_surface ,(580, 10))


def render():
	win.fill(WHITE)
	draw_grid()

	display_score()	

	for image in images:
		x, y, IMAGE = image
		win.blit(IMAGE, (x - IMAGE.get_width() // 2, y - IMAGE.get_height() // 2))

	pygame.display.update()
	

def main():
	global images

	images = []

	run = initialize_board()	
	render()

	while run:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			
			if event.type == pygame.MOUSEBUTTONDOWN:
				run = click()

		render()
	pygame.quit()
	sys.exit()

while True:
	if __name__ == '__main__':
		main()