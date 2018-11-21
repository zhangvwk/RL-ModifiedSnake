from QLearning import *
import pygame, random, sys
from pygame.locals import *
import time
import state_mapper as smp 

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
numIters = Setup.numIters
discount = Setup.discount
alpha = Setup.alpha
epsilon = Setup.epsilon

# Apple
apple = pygame.Surface((20, 20))  # size
apple.fill(GREEN)  # color
applePos = Apple(possiblePos_X, possiblePos_Y, x_snake, y_snake).position()

timeLimit = Setup.timeLimit
score = 0
highestScore = 0

snake_part = pygame.Surface((20, 20))
snake_part.fill(RED)

f = pygame.font.SysFont('Ubuntu', 20)
rl = QLearningAlgorithm(discount, alpha, blockPos)

""" GAME EXECUTION """

clock = pygame.time.Clock()
iteration = 1
count = 1
scoreList = [0]
initial = True

while True:

	# Stopping condition
	if iteration > numIters:
		break

	# Reset time and initial conditions when time's up
	timeStart = time.clock()
	currentTime = time.clock()
	x_snake, y_snake, direction, score = [140, 140, 140], [200, 180, 160], 'DOWN', 0

	# While time's not up
	while currentTime - timeStart < timeLimit:
		if iteration > numIters:
			break

		if count % 500 == 0:
			epsilon -= float(epsilon)/2
			print epsilon
			count = 1

		if epsilon < 0:
			epsilon = 0

		if highestScore > 15:
			clock.tick(20)
		# Computing the average score
		if len(scoreList) < 2:
			averageScore = 0
		if len(scoreList) >= 2 :
			averageScore = float(sum(scoreList))/(len(scoreList)-1)

		snakeLogic = GameLogic(applePos, blockPos, x_snake[0], y_snake[0])

		# Store the state as a string so it can used as a key in dict
		state = (x_snake, y_snake, applePos, direction)
		QuadrantView = smp.QuadrantView()
		mapped_state = QuadrantView.TransformState(x_snake, y_snake, applePos, blockPos, direction)
		action = rl.getAction(epsilon, mapped_state, Q)
		reward = rl.getReward(state, action)
		rl.updateQ(mapped_state, state, action, reward, Q, blockPos, initial)
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
			x_snake, y_snake, direction, score = [140, 140, 140], [200, 180, 160], 'DOWN', 0
			iteration += 1
			count += 1
			timeStart = time.clock()
			currentTime = time.clock()
			
		# Snake eats an apple
		if snakeLogic.eatsApple():
			score += 1
			x_snake.append(0)
			y_snake.append(0)
			# A new apple appears randomly
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

		for i in range(len(x_snake)):
			# Blit all the snake parts
			window.blit(snake_part, (x_snake[i], y_snake[i]))

		window.blit(apple, applePos)
		for i in range(numBlocks):
			window.blit(block, blockPos[i])

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
		currentTime = time.clock()

	if highestScore < score:
		highestScore = score

	scoreList.append(score)
	iteration += 1
	count += 1
pygame.time.wait(10000)