windowWidth = 400
windowHeight = 400
pixel = 20
int_width = int(windowWidth/pixel) - 1
int_height = int(windowHeight/pixel) - 1

# Setup colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
PURPLE = (139,0,139)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Q(state, action) dictionary
Q = {}