# Set Game
# 
# Alex Mak
import Card
import itertools
import sys

# one CardList represent a 2-D board
class Board:

	Rows = 3
	Cols = 4
	CardList = []
	DeckIndex = 0
	KnownSets = 0
	
	def __init__(self, Deck):
		self.Deck = Deck
		
		# distribute already shuffled deck
		for i in range(0,(self.Rows * self.Cols)):
			self.CardList.append(self.GetCardFromDeck())
				

	def CheckRemoveRow(self):
		if self.Rows != 4:
			return

		if self.CardList[12].isBlank() and self.CardList[13].isBlank() and self.CardList[14].isBlank() and self.CardList[15].isBlank():
			print("row 4 all used, remove row")
			self.RemoveRow()
		

	def ReplaceCard(self, index):
		# if 4th row is present, replace from there, and delete row if 4th row is all blank,
		# a click on any of the cards on row 4 can delete the row
		blankcard = Card.Card(0,0,0,0, -1)

		if (index >= 0):
			if (self.Rows == 4):
				#print("has row 4")
				card12 = self.CardList[12]
				if not card12.isBlank():
					self.CardList[index] = card12
					self.CardList[12] = blankcard
					print("replace 12")
					self.CheckRemoveRow()
					return

				card13 = self.CardList[13]
				if not card13.isBlank():
					self.CardList[index] = card13
					self.CardList[13] = blankcard
					print("replace 13")	
					self.CheckRemoveRow()
					return

				card14 = self.CardList[14]
				if not card14.isBlank():
					self.CardList[index] = card14
					self.CardList[14] = blankcard
					print("replace 14")	
					self.CheckRemoveRow()
					return
				
				card15 = self.CardList[15]
				if not card15.isBlank():
					self.CardList[index] = card15
					self.CardList[15] = blankcard
					print("replace 15")	
					self.CheckRemoveRow()
					return

			else:
				self.CardList[index] = self.GetCardFromDeck()


	def ReplaceCardsByIndex(self, indexes):
		self.ReplaceCard(indexes[0])
		self.ReplaceCard(indexes[1])
		self.ReplaceCard(indexes[2])
		count = self.CheckSetsIndex()
		if count == 0:
			print("after replace cards no sets, so add new row")
			self.AddRow()

	def GetCardFromDeck(self):

		#print (f"DeckIndex is at {self.DeckIndex}")

		if self.DeckIndex <= 80:
			self.DeckIndex = self.DeckIndex + 1
			return self.Deck[self.DeckIndex-1]

		print("return blank card")
		blank_card = Card.Card(0,0,0,0, 0)
		return blank_card

	"""
	A set consists of three cards satisfying all of these conditions:
	They all have the same number or have three different numbers.
	They all have the same shape or have three different shapes.
	They all have the same shading or have three different shadings.
	They all have the same color or have three different colors.

	If you can sort a group of three cards into "two of ____ and one of ____", then it is not a set.
	"""

	def IsSet(self, indexes):
		# get from the Board
		#print(f"IsSet() indexes: {indexes[0]} {indexes[1]} and {indexes[2]}")

		Card1 = self.CardList[indexes[0]]
		Card2 = self.CardList[indexes[1]]
		Card3 = self.CardList[indexes[2]]

		if Card1.shape == 0 and Card1.color == 0 and Card1.number == 0 and Card1.shading == 0:
			return False
		if Card2.shape == 0 and Card2.color == 0 and Card2.number == 0 and Card2.shading == 0:
			return False
		if Card3.shape == 0 and Card3.color == 0 and Card3.number == 0 and Card3.shading == 0:
			return False

		bSameShape = False
		bSameColor = False
		bSameNumber = False
		bSameShading = False

		if (Card1.shape == Card2.shape == Card3.shape):
			#print("same shape")
			bSameShape = True

		if (Card1.color == Card2.color == Card3.color):
			#print("same color")
			bSameColor = True

		if (Card1.number == Card2.number == Card3.number):
			#print("same number")
			bSameNumber = True

		if (Card1.shading == Card2.shading == Card3.shading):
			#print("same shading")
			bSameShading = True

		bAllDiffShape = True
		bAllDiffColor = True
		bAllDiffNumber = True
		bAllDiffShading = True

		if (Card1.shape == Card2.shape or 
			Card1.shape == Card3.shape or
			Card2.shape == Card3.shape ):
			bAllDiffShape = False

		if (Card1.color == Card2.color or 
			Card1.color == Card3.color or
			Card2.color == Card3.color ):
			bAllDiffColor = False

		if (Card1.number == Card2.number or 
			Card1.number == Card3.number or
			Card2.number == Card3.number ):
			bAllDiffNumber = False

		if (Card1.shading == Card2.shading or 
			Card1.shading == Card3.shading or
			Card2.shading == Card3.shading ):
			bAllDiffShading = False

		diffcount = 0
		if (bAllDiffShape):
			#print("all diff shape")
			diffcount += 1
		if (bAllDiffColor):
			#print("all diff color")
			diffcount += 1
		if (bAllDiffNumber):
			#print("all diff numbers")
			diffcount += 1
		if (bAllDiffShading):
			#print("all diff shading")
			diffcount += 1

		if ((bSameNumber == True or bAllDiffNumber == True) and
			(bSameShape == True or bAllDiffShape == True) and 
			(bSameShading == True or bAllDiffShading == True) and
			(bSameColor == True or bAllDiffColor == True)):

			print("A Set!!")
			print(Card1)
			print(Card2)
			print(Card3)
			print("-------")
		
			return True

		# 3 all different
		if (diffcount >= 4):

			print("A Set - all different !!")
			print(Card1)
			print(Card2)
			print(Card3)

			return True

		#print(diffcount)

		#print(Card1)
		#print(Card2)
		#print(Card3)

		#print("sorry, not a set")
		return False

	# Choose 3 cards, get the card's index
	def CheckSetsIndex(self):
		count = 0

		for combo in itertools.combinations(enumerate(self.CardList), 3):
			list = [*combo]
			index1 = [*list[0]]
			index2 = [*list[1]]
			index3 = [*list[2]]
			indexes = [index1[0], index2[0], index3[0]]

			if self.IsSet(indexes) == True:
				count += 1
		if count == 1:
			print("There is only 1 possible set on the table.")
		else:
			print ("There are " + str(count) + " possible sets on the table.")

		sys.stdout.flush()
		self.KnownSets = count
		return count

	def PrintDeck(self):
		i = 1

		with open("fulldeck.txt", "w") as f:
			for cc in self.Deck:
				print(cc.nth, end="", file = f)
				print(cc, end="", file = f)
				if i == self.DeckIndex:
					print("<-----", end = "", file = f)
				print(file = f)
				i = i + 1

	def PrintCardList(self):
		with open("table.txt", "w") as f:
			for cc in self.CardList:
				print(cc.nth, end="", file = f)
				print(cc, end="", file = f)
				print(file = f)
				
	def AddRow(self):
		# if there are matches do not allow add
		
		if self.KnownSets > 0:
			print(f'There are {self.KnownSets} sets so do not need to add row')
			return

		if self.DeckIndex >= 80:
			print("not adding rows - at end of deck")
			return
		self.Rows += 1

		self.CardList.append(self.GetCardFromDeck())
		self.CardList.append(self.GetCardFromDeck())
		self.CardList.append(self.GetCardFromDeck())
		self.CardList.append(self.GetCardFromDeck())
		
	def RemoveRow(self):

		if self.Rows == 4:
			self.Rows -= 1
		else:
			print("sorry, remove only if you have row 4")
			return
		
		card12 = self.CardList[12]
		card13 = self.CardList[13]
		card14 = self.CardList[14]
		card15 = self.CardList[15]

		if card12.isBlank() and card13.isBlank() and card14.isBlank() and card15.isBlank():
			print("removed 4 cells")
			self.CardList[-4] # remove 4 cells
		else:
			print("row 4 still have cells, so not removed")

		print(f"cardList now have {len(self.CardList)} cards")
