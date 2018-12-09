from initialization import *
from environment import *

def quadrant(coord):
	# Get the quadrant of coord = (x,y)
	q = [0, 0]
	for i in range(2):
		if coord[i] == 0:
			q[i] = 0
		elif coord[i] > 0:
			q[i] = 1
		else:
			q[i] = -1

	return (q[0], q[1])

def relativeQuadrant(coord, direction):
	# Get the relative quadrants given direction
	(x, y) = coord

	if direction == Directions.LEFT:
		(x, y) = ( y, -x)
	if direction == Directions.RIGHT:
		(x, y) = (-y,  x)
	if direction == Directions.DOWN:
		(x, y) = (-x, -y)

	return quadrant((x, y))

def hypoSquare(square, direction):
	(x, y) = square
	if direction == Directions.UP:
		return (x, y - pixel)
 	elif direction == Directions.DOWN:
		return (x, y + pixel)
	elif direction == Directions.LEFT:
		return (x - pixel, y)
	elif direction == Directions.RIGHT:
		return (x + pixel, y)

class QuadrantView:
	def __SquareDescription(self, snakeCoord_X, snakeCoord_Y, applePos, blockPos, square):
		""" Returns -1 if the square is a wall, snake_position, or a block.
			Returns 1 if it is a fruit. 0 otherwise."""
		snakeCoord = zip(snakeCoord_X, snakeCoord_Y)

		if square in blockPos or square in snakeCoord:
			return -1

		(x, y) = square
		if x < 0 or windowWidth - pixel < x:
			return -1
		if y < 0 or windowHeight - pixel < y:
			return -1

		if (x, y) == applePos:
			return 1

		return 0

	def mapState(self, snakeCoord_X, snakeCoord_Y, applePos, blockPos, direction):
		head = (snakeCoord_X[0], snakeCoord_Y[0])

		square_description = []
		for move in self.validMoves():
			transformed_direction = self.relativeMove(move, direction)
			n = hypoSquare(head, transformed_direction)
			square_description.append(self.__SquareDescription(snakeCoord_X, snakeCoord_Y, applePos, blockPos, n))
		head_ = (head[0], - head[1])
		applePos_ = (applePos[0], - applePos[1])

		(x, y) = (applePos_[0] - head_[0], applePos_[1] - head_[1])

		(qx, qy) = relativeQuadrant((x, y), direction)

		mapped_state = (square_description[0], square_description[1], square_description[2], qx, qy)

		return mapped_state

	def validMoves(self):
		return ['GO_LEFT', 'GO_RIGHT', 'GO_STRAIGHT']

	def relativeMove(self, move, direction):
		if move == 'GO_STRAIGHT':
			return direction

		if direction == Directions.UP:
			go_left_direction = Directions.LEFT
		if direction == Directions.DOWN:
			go_left_direction = Directions.RIGHT
		if direction == Directions.LEFT:
			go_left_direction = Directions.DOWN
		if direction == Directions.RIGHT:
			go_left_direction = Directions.UP

		if move == 'GO_LEFT':
			return go_left_direction
		elif move == 'GO_RIGHT':
			return Directions.REVERSE[go_left_direction]