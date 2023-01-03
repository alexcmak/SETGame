# Set Game
# project started 12/25/2022

class Card:

	def __init__(self, shape, color, number, shading, nth):
		self.shape = shape     # oval, squiggles, diamond
		self.color = color     # red, purple, green
		self.number = number   # 1, 2, 3
		self.shading = shading # solid, striped, outlined
		self.nth = nth         # nth card on the table

	def __str__(self):
		# python has no switch case
		s_shape = 'unknown'
		if (self.shape == 1):
			s_shape = 'Oval'
		elif (self.shape == 2):
			s_shape = 'Squiggles'
		elif (self.shape == 3):
			s_shape = 'Diamond'

		s_color = 'unknown'
		if (self.color == 1):
			s_color = 'Red'
		elif (self.color == 2):
			s_color = 'Purple'
		elif (self.color == 3):
			s_color = 'Green'

		s_shading = 'unknown'
		if (self.shading == 1):
			s_shading = 'Solid'
		elif (self.shading == 2):
			s_shading = 'Striped'
		elif (self.shading == 3):
			s_shading = 'Outlined'

		if self.isBlank():
			string_representation = "[      ---- Blank ----      ]"
		else:
			string_representation = f"[{s_shape:<9} {s_color:<6} {self.number} {s_shading:<8}]"

		return string_representation

	def isBlank(self):
		if self.shape == 0 and self.color == 0 and self.number == 0 and self.shading == 0:
			return True
		return False

