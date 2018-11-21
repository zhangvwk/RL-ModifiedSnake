import random
import math
from initialization import *

# random.seed(40)

class Directions:
	UP = 'UP'
	DOWN = 'DOWN'
	RIGHT = 'RIGHT'
	LEFT = 'LEFT'
	ALL = [UP, DOWN, LEFT, RIGHT]
	REVERSE = {UP: DOWN, DOWN: UP, LEFT: RIGHT, RIGHT: LEFT}

class Setup:
	# Initial snake coordinates from head to tail
	snakeCoord_X = [140, 140, 140]
	snakeCoord_Y = [200, 180, 160]
	numIters = 100000
	timeLimit = 1000000
	# Initial direction
	direction = random.choice(Directions.ALL)
	# Learning parameters
	discount = 0.9
	alpha = 0.8
	epsilon = 0.6

class Block:
	def __init__(self, numBlocks):
		self.numBlocks = numBlocks

	# Returns list of block-unoccupied x and y coordinates
	def unoccupied(self):
		numBlocks = self.numBlocks
		# blockPos_normalized = [(random.randint(1, 14), random.randint(0, 14)) for i in range(numBlocks)]
		blockPos_normalized = [(7, 13), (1, 4), (14, 9), (2, 5), (13, 6), (1, 13), (2, 9), (9, 6), (14, 2), (9, 1), (14, 2), (8, 12), (13, 1), (13, 12), (5, 11), (4, 2), (3, 4), (12, 6), (14, 13), (3, 6)]
		# blockPos_normalized = [(1000,1000),(1000,1000),(1000,1000),(1000,1000),(1000,1000),(1000,1000),(1000,1000),(1000,1000),(1000,1000),(1000,1000),(1000,1000),(1000,1000),(1000,1000),(1000,1000),]
		blockPos = [(blockPos_normalized[i][0]*pixel, blockPos_normalized[i][1]*pixel) for i in range(numBlocks)]
		blockPos_X = set(blockPos_normalized[i][0] for i in range(numBlocks))
		blockPos_Y = set(blockPos_normalized[i][1] for i in range(numBlocks))
		possiblePos_X = list(set(i for i in range(14)) - blockPos_X)
		possiblePos_Y = list(set(i for i in range(14)) - blockPos_Y)
		return blockPos, possiblePos_X, possiblePos_Y

class Apple:
	def __init__(self, possiblePos_X, possiblePos_Y, snakeCoord_X, snakeCoord_Y):
		self.possiblePos_X = possiblePos_X
		self.possiblePos_Y = possiblePos_Y
		self.snakeCoord_X = snakeCoord_X
		self.snakeCoord_Y = snakeCoord_Y

	def position(self):
		# Apple coordinates that fits
		possiblePos_X = self.possiblePos_X
		possiblePos_Y = self.possiblePos_Y
		snakeCoord_X = self.snakeCoord_X
		snakeCoord_Y = self.snakeCoord_Y
		applePos = (random.choice(possiblePos_X)*pixel, random.choice(possiblePos_Y)*pixel)
		while applePos in zip(snakeCoord_X, snakeCoord_Y):
			applePos = (random.choice(possiblePos_X)*pixel, random.choice(possiblePos_Y)*pixel)
		return applePos

class GameLogic:
	def __init__(self, applePos, obstaclePos, snakeHead_X, snakeHead_Y):
		self.applePos = applePos
		self.obstaclePos = obstaclePos
		self.snakeHead_X = snakeHead_X
		self.snakeHead_Y = snakeHead_Y

	def collisionWall(self):
		snakeHead_X = self.snakeHead_X
		snakeHead_Y = self.snakeHead_Y 
		# print 'hit wall'
		return snakeHead_X < 0 or snakeHead_X >= windowWidth or snakeHead_Y < 0 or snakeHead_Y >= windowHeight

	def collisionObstacle(self):
		obstaclePos = self.obstaclePos
		snakeHead_X = self.snakeHead_X
		snakeHead_Y = self.snakeHead_Y
		# print 'hit block'
		return (snakeHead_X, snakeHead_Y) in obstaclePos

	def eatsApple(self):
		applePos = self.applePos
		snakeHead_X = self.snakeHead_X
		snakeHead_Y = self.snakeHead_Y
		return snakeHead_X == applePos[0] and snakeHead_Y == applePos[1]