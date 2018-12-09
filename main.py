from QLearning import *
from sarsa import *
import pygame, random, sys
from pygame.locals import *
import time
import state_mapper as smp
import csv

""" SETUP """

pygame.init()
window = pygame.display.set_mode([windowWidth, windowHeight])
pygame.display.set_caption('Snake')

# Blocks
block = pygame.Surface((20,20))
block.fill(PURPLE)
numBlocks = 10
blockPos, possiblePos_X, possiblePos_Y = Block(numBlocks).unoccupied()

# Snake
x_snake = Setup.snakeCoord_X
y_snake = Setup.snakeCoord_Y
direction = Setup.direction
trainIters = Setup.trainIters
testIters = Setup.testIters
discount = Setup.discount
alpha = Setup.alpha
epsilon_u = Setup.epsilon_u
epsilon_l = Setup.epsilon_l

# Apple
apple = pygame.Surface((20, 20))  # size
apple.fill(GREEN)  # color
applePos = Apple(possiblePos_X, possiblePos_Y, x_snake, y_snake).position()

score = 0
highestScore = 0

snake_part = pygame.Surface((20, 20))
snake_part.fill(RED)

f = pygame.font.SysFont('Ubuntu', 20)

# Choose the RL agent
agent = 'QL'
# agent = 'SARSA'

if agent == 'QL':
	rl = QLearningAlgorithm(discount, alpha, blockPos)
elif agent == 'SARSA':
	rl = SARSAAlgorithm(discount, alpha, blockPos)

# 1 for training and 0 for testing
training = 1

if training:
	file = 'training_'
	timeLimit = Setup.training_timeLimit
elif not training:
	file = 'testing_'
	timeLimit = Setup.testing_timeLimit

file += agent + '_' + str(epsilon_u) + '.csv'

""" GAME EXECUTION """

clock = pygame.time.Clock()
iteration = 1
count = 1
scoreList = [0]
initial = True
epsilon = epsilon_u # Start epsilon at the upper bound

with open(file, 'wb') as csvfile:
	while True:
		if training:
			# Stopping condition
			if iteration > trainIters:
				break

		elif not training:
			if iteration > testIters:
				break

		# Reset frame and initial conditions when time's up
		frame = 1
		currentTime = time.clock()
		x_snake, y_snake, direction, score = [140, 140, 140], [200, 180, 160], 'DOWN', 0

		# While time's not up
		while frame < timeLimit:
			if training:
				if iteration > trainIters:
					rl.writePolicy(Q, epsilon_u)
					break
			elif not training:
				if iteration > testIters:
					break
			if iteration > 5000:
				clock.tick(fps)
			
			# Decay epsilon 
			if count % 500 == 0:
				# Divide it by 2 every 500 iterations
				epsilon -= float(epsilon)/2
				count = 1

			# Lower bound epsilon by epsilon_l if epsilon is not 0
			if epsilon < epsilon_l and epsilon != 0:
				epsilon = epsilon_l

			if len(scoreList) < 2:
				averageScore = 0
			if len(scoreList) >= 2 :
				averageScore = float(sum(scoreList))/(len(scoreList)-1)

			snakeLogic = GameLogic(applePos, blockPos, x_snake[0], y_snake[0])

			# Observe state
			state = (x_snake, y_snake, applePos, direction)
			QuadrantView = smp.QuadrantView()
			mapped_state = QuadrantView.TransformState(x_snake, y_snake, applePos, blockPos, direction)

			# If we want to train the agent
			if training:
				# Choose new action according to Q
				# and the exploration strategy
				action = rl.getAction(epsilon, mapped_state, Q)
				
				# Observe reward
				reward = rl.getReward(state, action)

				# Update the Q table
				if agent == 'QL':
					rl.updateQ(mapped_state, state, action, reward, Q, blockPos, initial) # For Q-Learning
				elif agent == 'SARSA':
					rl.updateQ(mapped_state, state, action, reward, Q, blockPos, initial, epsilon) # For SARSA

			elif not training:
				action = rl.getAction(epsilon, mapped_state, Q)

			initial = False
			move = QuadrantView.TransformMove(action, direction)

			direction = move

			# Test if snake hits itself
			hitItself = False
			i = len(x_snake) - 1
			while i >= 3:
				if x_snake[0] == x_snake[i] and y_snake[0] == y_snake[i]:
					hitItself = True
					break
				i -= 1

			# Snake hits itselfa a wall or an obstacle
			if hitItself or snakeLogic.collisionObstacle() or snakeLogic.collisionWall():
				scoreList.append(score)

				# Update the score and iteration in the .csv file
				filewriter = csv.writer(csvfile, delimiter=',',
															quotechar='|', quoting=csv.QUOTE_MINIMAL)
				filewriter.writerow([iteration, score, epsilon, averageScore, timeout])
				
				x_snake, y_snake, direction, score = [140, 140, 140], [200, 180, 160], 'DOWN', 0

				iteration += 1
				count += 1
				timeStart = time.clock()
				currentTime = time.clock()
				# Reset the blocks positions
				blockPos, possiblePos_X, possiblePos_Y = Block(numBlocks).unoccupied()
				frame = 1
				
			# Snake eats an apple
			if snakeLogic.eatsApple():
				score += 1
				x_snake.append(0)
				y_snake.append(0)
				# Reset the apple position
				applePos = Apple(possiblePos_X, possiblePos_Y, x_snake, y_snake).position()

			# Update the snake tail coordinates
			i = len(x_snake) - 1
			while i >= 1:
				x_snake[i] = x_snake[i-1]
				y_snake[i] = y_snake[i-1]
				i -= 1

			# Update the snake head coordinates
			if direction == 'DOWN':
				y_snake[0] += pixel
			elif direction == 'RIGHT':
				x_snake[0] += pixel
			elif direction == 'UP':
				y_snake[0] -= pixel
			elif direction == 'LEFT':
				x_snake[0] -= pixel

			# Background color	
			window.fill(BLACK)
				
			# Blit all the snake parts
			for i in range(len(x_snake)):
				window.blit(snake_part, (x_snake[i], y_snake[i]))

			# Blit the apple
			window.blit(apple, applePos)

			# Blit all the blocks
			for i in range(numBlocks):
				window.blit(block, blockPos[i])

			# Keep track of the highest score
			# obtained thus far
			if highestScore < score:
				highestScore = score
			
			scoreRender = f.render('Score: ' + str(score), True, WHITE)
			recordRender = f.render('Highest score: ' + str(highestScore), True, WHITE)
			epsilonRender = f.render('Epsilon: ' + str(epsilon), True, WHITE)
			iterationRender = f.render('Iteration: ' + str(iteration), True, WHITE)
			averageScoreRender = f.render('Average score: ' + str(averageScore), True, WHITE)
 
			window.blit(recordRender, (10, 10))
			window.blit(scoreRender, (10, 40))
			window.blit(epsilonRender, (270, windowHeight - 50))
			window.blit(iterationRender, (100, windowHeight - 50))
			window.blit(averageScoreRender, (100, windowHeight - 20))

			pygame.display.update()
			frame += 1
			timeout = 0

		if highestScore < score:
			highestScore = score

		timeout += 1
		scoreList.append(score)
		iteration += 1
		count += 1

pygame.time.wait(1000)