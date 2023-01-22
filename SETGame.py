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
SetCount = 0
PossibleMatches = 0
ShowHelpBox = False
HintCount = 0

# Screen
WIDTH = 750
ROWS = 4
win = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("SET Game - Alex Mak")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
YELLOW = (255, 191, 0)

SCORE_FONT = pygame.font.SysFont("Comic Sans MS", 20)
END_FONT = pygame.font.SysFont('courier', 40)

# Images
image_w = 170
image_h = 100

b = None
PNGS = []

Score_message = ""

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
		
	images.clear()

	i = 0
	for r in range(0, b.Rows):
		row = r * box_size + image_h - offset
		for c in range(0, 4):
			if row == 4:
				images.append((c * box_size + col,row, PNGS[0]))
			else:
				images.append((c * box_size + col,row, card_image(i)))
				i+= 1

	#print(f"there are {b.Rows} rows")
	#b.PrintTable()

def initialize_board():
	global b
	global PossibleMatches
	global SetCount
	global Score_message
	global HintCount

	SetCount = 0
	PossibleMatches = 0
	boxes_clicked.clear()
	Deck.clear()
	Score_message = ""
	HintCount = 0
	
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
	# b.PrintDeck()

	PossibleMatches = b.CheckSetsIndex()

	if PossibleMatches == 0:
		print("Whoa unusual, need 4th row")
		b.AddRow()
		PossibleMatches = b.CheckSetsIndex()
		if PossibleMatches == 0:
			game_over()
			return False


	distribute_cards()
	return True
	
boxes_clicked = []

def OnClicked():
	global images
	global click_count
	global b
	global SetCount
	global PossibleMatches

	# Mouse position
	m_x, m_y = pygame.mouse.get_pos()
	box_size = WIDTH / 4
	box_clicked = -1

	if (len(boxes_clicked) == 3):
		boxes_clicked.clear()

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

	if box_clicked not in boxes_clicked:
		boxes_clicked.append(box_clicked)

	return True

def game_over():
	pygame.time.delay(500)
	win.fill(WHITE)
	end_text = END_FONT.render("Game Over", 1, BLACK)

	mid_width = (WIDTH - end_text.get_width()) // 2
	mid_height = (WIDTH - end_text.get_height()) // 2

	win.blit(end_text, (mid_width, mid_height - 50 ))
	score_text = SCORE_FONT.render(Score_message, False, BLACK)
	win.blit(score_text, (mid_width,mid_height + 35))

	hint_message = "Hints needed: " + str(HintCount)
	hint_text = SCORE_FONT.render(hint_message, False, BLACK)
	win.blit(hint_text, (mid_width,mid_height + 80))

	pygame.display.update()
	pygame.time.delay(7000)
	initialize_board()


def display_score():

	global SetCount
	global PossibleMatches
	global Score_message

	if (SetCount == 1):
		Score_message = "Score: " + str(SetCount) + " set"
	elif (SetCount > 1):
		Score_message = "Score: " + str(SetCount) + " sets"
	
	score_text = SCORE_FONT.render(Score_message, False, BLACK)
	win.blit(score_text, (10,10))

	possible_text = ""
	if (PossibleMatches == 1):
		possible_text = str(PossibleMatches) + " set possible"
	elif (PossibleMatches > 1):
		possible_text = str(PossibleMatches) + " sets possible"

	possible_surface = SCORE_FONT.render(possible_text, False, BLACK)
	win.blit(possible_surface ,(580, 10))

def draw_box(box_clicked, color):
	grid_width = WIDTH / 4
	box_size = grid_width * 0.9
	offset = 9

	col_clicked = int(box_clicked % 4)
	row_clicked = box_clicked // 4

	x = col_clicked * (box_size + 2* offset) + offset
	y = row_clicked * (box_size + 2* offset) + offset

	pygame.draw.rect(win, color, pygame.Rect(x, y, box_size, box_size), 2)
	return

def draw_boxes():

	for box in boxes_clicked:
		draw_box(box, BLACK)

	if ShowHelpBox == True:
		for box in b.Match_indexes:
			draw_box(box, YELLOW)

	return

def render():
	win.fill(WHITE)
	draw_grid()

	display_score()	

	for image in images:
		x, y, IMAGE = image
		win.blit(IMAGE, (x - IMAGE.get_width() // 2, y - IMAGE.get_height() // 2))

	draw_boxes()

	pygame.display.update()

def check_match():

	global SetCount
	global PossibleMatches 

	num_boxes_clicked = len(boxes_clicked)

	#b.PrintTable()

	if (num_boxes_clicked == 3):
		print(boxes_clicked)
		if b.IsSet(boxes_clicked) == True:
			print("got a set!")
			SetCount += 1
			b.ReplaceCardsByIndex(boxes_clicked)
			#b.PrintDeck()

			PossibleMatches = b.CheckSetsIndex()

			distribute_cards()
			if b.DeckIndex >= 81:
				game_over()
				return False
		else:
			print("sorry that was not a set")

		pygame.time.delay(500)
		boxes_clicked.clear()	
	#else:
	#	print("sorry do not have 3 boxes")

def main():
	global images
	global ShowHelpBox
	global HintCount
	images = []

	load_images()
	run = initialize_board()
	render()

	while run:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == pygame.BUTTON_LEFT:
					run = OnClicked()
				elif event.button == pygame.BUTTON_RIGHT:
					ShowHelpBox = True

			if event.type == pygame.MOUSEBUTTONUP:
				if event.button == pygame.BUTTON_RIGHT:
					HintCount += 1
					ShowHelpBox = False

		
		render()
		check_match()
		

	pygame.quit()
	sys.exit()

while True:
	if __name__ == '__main__':
		main()