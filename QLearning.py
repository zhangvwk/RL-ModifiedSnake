from environment import *
import state_mapper as smp
import collections 
from numpy.random import choice

QuadrantView = smp.QuadrantView()

class QLearningAlgorithm:
	def __init__(self, discount, alpha, blockPos):
		self.alpha = alpha
		self.discount = discount
		# self.epsilon = epsilon
		self.blockPos = blockPos

	def hypoSnakeHead(self, state, move):
		snakeCoord_X, snakeCoord_Y = state[0:2]

		if move == Directions.DOWN:
			snakeHead_Y = snakeCoord_Y[0] + pixel
			snakeHead_X = snakeCoord_X[0]
		elif move == Directions.RIGHT:
			snakeHead_X = snakeCoord_X[0] + pixel
			snakeHead_Y = snakeCoord_Y[0]
		elif move == Directions.UP:
			snakeHead_Y = snakeCoord_Y[0] - pixel
			snakeHead_X = snakeCoord_X[0]
		elif move == Directions.LEFT:
			snakeHead_X = snakeCoord_X[0] - pixel
			snakeHead_Y = snakeCoord_Y[0]

		return (snakeHead_X, snakeHead_Y)

	def actions(self):
		return QuadrantView.GetAllowedMoves()

	# Epsilon-greedy exploration strategy
	def getAction(self, epsilon, mapped_state, QValues):

		# Initialize Q values at 0
		if mapped_state not in QValues.keys():
			QValues[mapped_state] = {}
			for action_ in self.actions():
				QValues[mapped_state][action_] = 10

		if random.random() < epsilon:
			return random.choice(self.actions())
		else:
			return max((self.getQ(mapped_state, action, QValues), action) \
									for action in self.actions())[1]

		# SOFTMAX NOT WORKING
		# T = 3
		# SUM = sum([float(math.exp(self.getQ(mapped_state, action, QValues)))/T \
		# 			for action in self.actions()])
		# prob = [float((float(math.exp(self.getQ(mapped_state, action, QValues)))/T))/SUM for action in self.actions()]
		# draw = choice(prob)
		# action_idx = prob.index(draw)
		# return self.actions()[action_idx]


	def getReward(self, state, action):
		blockPos = self.blockPos

		x_snake, y_snake, applePos, direction = state
		move = QuadrantView.TransformMove(action, direction)
		snakeHead_X, snakeHead_Y = self.hypoSnakeHead(state, move)
		snakeLogic = GameLogic(applePos, blockPos, snakeHead_X, snakeHead_Y)

		# Test if snake hits itself
		hitItself = False
		i = len(x_snake) - 1
		while i >= 2:
			if snakeHead_X == x_snake[i] and snakeHead_Y == y_snake[i]:
				hitItself = True
				break
			i -= 1

		# Snake hits itselfa a wall or an obstacle
		if hitItself or snakeLogic.collisionObstacle() or snakeLogic.collisionWall():
			return -100
			
		# Snake eats an apple
		if snakeLogic.eatsApple():
			return 500

		# Encourage the snake to go to the apple quickly
		else:
			return -10

	def getQ(self, mapped_state, action, QValues):
		return QValues[mapped_state][action]


	def getState(self, state, action):
		direction = state[3]
		move = QuadrantView.TransformMove(action, direction)
		x_snake, y_snake = state[0:2]
		x_snakeCopy, y_snakeCopy = x_snake[:], y_snake[:]

		i = len(x_snake) - 1
		while i >= 1:
			x_snakeCopy[i] = x_snakeCopy[i-1]
			y_snakeCopy[i] = y_snakeCopy[i-1]
			i -= 1

		if move == 'DOWN':
			y_snakeCopy[0] += pixel
		elif move == 'RIGHT':
			x_snakeCopy[0] += pixel
		elif move == 'UP':
			y_snakeCopy[0] -= pixel
		elif move == 'LEFT':
			x_snakeCopy[0] -= pixel

		return (x_snakeCopy, y_snakeCopy, state[2], move)

	def updateQ(self, mapped_state, state, action, reward, QValues, blockPos, initial):
		
		# First step
		if initial:
			return

		direction = state[3]

		alpha = self.alpha
		discount = self.discount
		applePos = state[2]

		q = QValues[mapped_state][action]

		# If snake dies
		if reward == -100:
			q += alpha * (reward - q)

		else:
			new_state = self.getState(state, action)
			move = QuadrantView.TransformMove(action, direction)
			new_mapped_state = QuadrantView.TransformState(new_state[0], new_state[1], \
																										new_state[2], blockPos, move)

			# Initialize Q values at 0
			if new_mapped_state not in QValues.keys():
				QValues[new_mapped_state] = {}
				for newAction in self.actions():
					QValues[new_mapped_state][newAction] = 10

			# Off-policy
			max_q = max(QValues[new_mapped_state].values())

			# Temporal difference
			q += alpha*(reward + discount*max_q - q)

		QValues[mapped_state][action] = q 

	def writePolicy(self, QValues, epsilon_u):
		policyFile = 'QL_' + str(epsilon_u) + '.policy'
		with open(policyFile, 'w') as f:
			f.write(str(QValues))
		return