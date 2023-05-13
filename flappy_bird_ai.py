#######################
# import libraries
#######################

import os
import random
import time

import neat  # (NeuroEvolution of Augmenting Topologies)
import pygame

pygame.font.init()

#######################
# set the graphical window and load the images
#######################

# set the const window width and height
WIN_WIDTH = 500
WIN_HEIGHT = 800
# create the game window with the given dimensions
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
# set the title of the game
pygame.display.set_caption("Flappy Bird")
# load the bird images and scale them 2 times for clarity
BIRD_IMGS = [
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png"))),
]
# load the pipe image and scale them 2 times for clarity
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
# load the base image and scale them 2 times for clarity
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
# load the background image and scale them 2 times for clarity
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))
# get the font for displaying the score
STAT_FONT = pygame.font.SysFont("comicsans", 25)
END_FONT = pygame.font.SysFont("comicsans", 70)
DRAW_LINES = False
FLOOR = 703

gen = 0

#######################
# create the class
#######################


class Bird:
    """
    Bird class representing the flappy bird
    """

    # 'IMGS': This constant holds a collection of bird images that will be used to animate the bird's motion
    # 'MAX_ROTATION': This constant sets the maximum angle (in degrees) that the bird can rotate upward or downward
    # 'ROT_VEL': This constant represents the rate at which the bird rotates per frame
    # 'ANIMATION_TIME': This constant represents the number of frames that will be displayed for each bird animation
    # It may be used to control the speed of the bird's wing flapping animation

    IMGS = BIRD_IMGS
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        """
        Initialize the object
        :param x: starting x pos (int)
        :param y: starting y pos (int)
        :return: None
        """
        # initialized to the corresponding x and y arguments passed into the constructor
        self.x = x
        self.y = y
        # the current angle of the bird's tilt (in degrees)
        self.tilt = 0
        # the number of frames that have elapsed since the bird's last jump
        self.tick_count = 0
        # the current vertical velocity of the bird
        self.vel = 0
        # the bird's current height on the screen
        self.height = self.y
        # the index of the current bird image being displayed
        self.img_count = 0
        # the current bird image being displayed
        self.img = self.IMGS[0]

    def jump(self):
        """
        make the bird jump
        :return: None
        """
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        """
        make the bird move
        :return: None
        """
        # one more frame has elapsed since the bird's last jump
        self.tick_count += 1
        # calculate the vertical displacement of the bird using equation d = vt + (1/2)at^2
        d = self.vel * self.tick_count + 1.5 * self.tick_count**2
        # caps the bird's downward velocity at a maximum value of 16 pixels per frame
        if d >= 16:
            d = 16
        #  set a minimum upward velocity of -2 pixels per frame
        if d < 0:
            d = -2
        # updates the bird's y coordinate by adding the calculated displacement d to its current y position
        self.y = self.y + d
        # check if the bird is still moving upward or if it has passed its maximum height
        if d < 0 or self.y < self.height + 50:
            # set the bird's tilt angle to the maximum rotation value if it hasn't already reached that angle
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
            else:
                # decreases the bird's tilt angle if the bird is not tilted at the maximum angle
                if self.tilt > -90:
                    self.tilt -= self.ROT_VEL

    def draw(self, win):
        """
        draw the bird
        :param win: pygame window or surface
        :return: None
        """
        # one more frame has elapsed since the bird's last animation frame
        self.img_count += 1
        # determine which image of the bird to draw
        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME * 2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME * 3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME * 4:
            self.img = self.IMGS[1]
            # reset to 0 and the animation starts over
        elif self.img_count < self.ANIMATION_TIME * 4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0
        # check if the bird is in nosedive and draw the image with non-flapping wings
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME * 2

        # tilt the bird
        blitRotateCenter(win, self.img, (self.x, self.y), self.tilt)

    def get_mask(self):
        """
        gets the mask for the current image of the bird
        :return: None
        """
        # used for collision detection with other objects in the game, such as pipes or the ground.
        return pygame.mask.from_surface(self.img)


class Pipe:
    """
    represents a pipe object
    """

    # 'GAP': This constant sets the gap between top and bottom pipes
    # 'VEL': This constant sets the velocity at which the pipes move
    GAP = 200
    VEL = 5

    def __init__(self, x):
        """
        initialize pipe object
        :param x: int
        :param y: int
        :return" None
        """
        # initialized to the corresponding x argument passed into the constructor
        self.x = x
        # the height of the gap between the top and bottom pipes
        self.height = 0

        # the y-coordinates of the top and bottom pipes respectively
        self.top = 0
        self.bottom = 0
        # the surface image of the top pipe, flipped vertically
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        # the surface image of the bottom pipe
        self.PIPE_BOTTOM = PIPE_IMG
        # a boolean flag indicating whether the bird has passed the pipe
        self.passed = False
        self.set_height()

    def set_height(self):
        """
        set the height of the pipe, from the top of the screen
        :return: None
        """
        # generate a random height in the range
        self.height = random.randrange(50, 450)
        # calculate the top and bottom positions
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        """
        move pipe based on vel
        :return: None
        """
        # update the position of the pipe
        self.x -= self.VEL

    def draw(self, win):
        """
        draw both the top and bottom of the pipe
        :param win: pygame window/surface
        :return: None
        """
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird, win):
        """
        returns if a point is colliding with the pipe
        :param bird: Bird object
        :return: Bool
        """
        # get the masks for the bird, top and bottom pipes respectively
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)
        # calculate the offset between the bird's position and the pipe's position
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))
        # calculate the collision point of the bird's mask and the top pipe's mask or the bottom pipe's mask respectively
        top_point = bird_mask.overlap(top_mask, top_offset)
        bottom_point = bird_mask.overlap(bottom_mask, bottom_offset)

        if top_point or bottom_point:
            # there is a collision
            return True
        # there is no collision
        return False


class Base:
    """
    Represnts the moving floor of the game
    """

    # 'VEL': This constant sets the velocity at which the base move
    # 'WIDTH': This constant holds the width of the base image
    # 'IMG': This constant holds the base image that will be used to animate the base's motion

    VEL = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y):
        """
        Initialize the object
        :param y: int
        :return: None
        """
        # initialized to the corresponding y argument passed into the constructor
        self.y = y
        # initialize the x coordinate of the first base image to 0
        self.x1 = 0
        # initialize the x coordinate of the second base image to the width of the base image
        self.x2 = self.WIDTH

    def move(self):
        """
        move floor so it looks like its scrolling
        :return: None
        """
        # update the positions of the two base images by decrementing their x-coordinates
        self.x1 -= self.VEL
        self.x2 -= self.VEL
        # left edge of the first base image has moved completely off the left side of the screen
        if self.x1 + self.WIDTH < 0:
            # reset its position to the right edge of the second base image (swapping their position)
            self.x1 = self.x2 + self.WIDTH
        # left edge of the second base image has moved completely off the left side of the screen
        if self.x2 + self.WIDTH < 0:
            # reset its position to the right edge of the first base image (swapping their position)
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        """
        Draw the floor. This is two images that move together.
        :param win: the pygame surface/window
        :return: None
        """
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))


def blitRotateCenter(surf, image, topleft, angle):
    """
    Rotate a surface and blit it to the window
    :param surf: the surface to blit to
    :param image: the image surface to rotate
    :param topLeft: the top left position of the image
    :param angle: a float value for angle
    :return: None
    """
    # create a new image by rotating the current image by the bird's current tilt angle
    rotated_image = pygame.transform.rotate(image, angle)
    # create a new rectangle that is centered at the same point as the original image
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=topleft).center)
    # draw the rotated image on the game window at the topleft corner of the new rectangle
    surf.blit(rotated_image, new_rect.topleft)


#######################
# draw the graphical window
#######################


def draw_window(win, birds, pipes, base, score, gen, pipe_ind):
    """
    draws the windows for the main game loop
    :param win: pygame window surface
    :param bird: a Bird object
    :param pipes: List of pipes
    :param score: score of the game (int)
    :param gen: current generation
    :param pipe_ind: index of closest pipe
    :return: None
    """
    # draw the background image at the topleft corner of the game window, which effectively clears the window before redrawing the bird.
    if gen == 0:
        gen = 1
    win.blit(BG_IMG, (0, 0))

    for pipe in pipes:
        # draw the pipe image on the game window
        pipe.draw(win)

    base.draw(win)
    for bird in birds:
        # draw lines from bird to pipe
        if DRAW_LINES:
            try:
                pygame.draw.line(
                    win,
                    (255, 0, 0),
                    (
                        bird.x + bird.img.get_width() / 2,
                        bird.y + bird.img.get_height() / 2,
                    ),
                    (
                        pipes[pipe_ind].x + pipes[pipe_ind].PIPE_TOP.get_width() / 2,
                        pipes[pipe_ind].height,
                    ),
                    5,
                )
                pygame.draw.line(
                    win,
                    (255, 0, 0),
                    (
                        bird.x + bird.img.get_width() / 2,
                        bird.y + bird.img.get_height() / 2,
                    ),
                    (
                        pipes[pipe_ind].x + pipes[pipe_ind].PIPE_BOTTOM.get_width() / 2,
                        pipes[pipe_ind].bottom,
                    ),
                    5,
                )
            except:
                pass
        # draw bird
        bird.draw(win)

    # score
    score_label = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
    win.blit(score_label, (WIN_WIDTH - score_label.get_width() - 15, 10))

    # generations
    score_label = STAT_FONT.render("Gens: " + str(gen - 1), 1, (255, 255, 255))
    win.blit(score_label, (10, 10))

    # alive
    score_label = STAT_FONT.render("Alive: " + str(len(birds)), 1, (255, 255, 255))
    win.blit(score_label, (10, 50))

    # update the game window to show the newly drawn images
    pygame.display.update()


#######################
# NEAT implementation
#######################


def eval_genomes(genomes, config):
    """
    runs the simulation of the current population of
    birds and sets their fitness based on the distance they
    reach in the game.
    """
    global WIN, gen
    win = WIN
    gen += 1

    # initialize a neural network list
    nets = []
    # initialize a genome list
    ge = []
    # initialize a bird list
    birds = []

    for genome_id, genome in genomes:
        # start with fitness level of 0
        genome.fitness = 0
        # a neural network is created using the current genome and the configuration file
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        birds.append(Bird(230, 350))
        ge.append(genome)

    base = Base(FLOOR)
    pipes = [Pipe(WIN_WIDTH)]
    # create a clock object to control the frame rate of the game
    clock = pygame.time.Clock()
    # initilize the score to 0
    score = 0
    # initialize the game loop variable
    run = True
    while run and len(birds) > 0:
        # limit the frame rate of the game to 30 frames per second
        clock.tick(30)
        # check if the user has quit the game by clicking the close button on the game window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                # quit the pygame module
                pygame.quit()
                # terminate the python interpreter
                quit()
                break

        # select which pipe to use as the reference pipe for the birds
        pipe_ind = 0
        # any birds left
        if len(birds) > 0:
            if (
                # at least 2 pipes in the pipes list
                len(pipes) > 1
                and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width()
            ):
                # second pipe in the list will be the reference pipe for the birds
                pipe_ind = 1

        for x, bird in enumerate(birds):
            # give each bird a fitness of 0.1 for each frame it stays alive
            ge[x].fitness += 0.1
            # update the position of the bird
            bird.move()

            # send bird location, top pipe location and bottom pipe location and determine from network whether to jump or not
            output = nets[birds.index(bird)].activate(
                (
                    bird.y,
                    abs(bird.y - pipes[pipe_ind].height),
                    abs(bird.y - pipes[pipe_ind].bottom),
                )
            )
            # a tanh activation function is used, so result will be between -1 and 1. if over 0.5 jump
            if output[0] > 0.5:
                bird.jump()
        # update the position of the base
        base.move()

        # initiliaze the added pipe
        add_pipe = False
        # empty list that will contain pipes that have gone off-screen
        rem = []
        for pipe in pipes:
            # update the position of the pipe
            pipe.move()
            for bird in birds:
                if pipe.collide(bird, win):
                    # fitness is decreased
                    ge[birds.index(bird)].fitness -= 1
                    # removed from the list of birds, its corresponding neural network and genome
                    nets.pop(birds.index(bird))
                    ge.pop(birds.index(bird))
                    birds.pop(birds.index(bird))

            # moved completely off the left side of the screen
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                # append index to rem
                rem.append(pipe)

            # not yet been passed by the bird and the bird has passed the left edge of the pipe
            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True

        if add_pipe:
            # score is incremented
            score += 1
            for genome in ge:
                genome.fitness += 5
            # set the new pipe
            pipes.append(Pipe(WIN_WIDTH))
        # if rem is not empty
        for r in rem:
            # each pipe in rem is removed from pipes
            pipes.remove(r)

        for bird in birds:
            if bird.y + bird.img.get_height() - 10 >= FLOOR or bird.y < 0:
                # removed from the list of birds, its corresponding neural network and genome
                nets.pop(birds.index(bird))
                ge.pop(birds.index(bird))
                birds.pop(birds.index(bird))

        # redraw the game window with the updated background and bird images
        draw_window(WIN, birds, pipes, base, score, gen, pipe_ind)


def run(config_file):
    """
    runs the NEAT algorithm to train a neural network to play flappy bird.
    :param config_file: location of config file
    :return: None
    """
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_file,
    )

    # the population of genomes that will be evolved by the algorithm
    p = neat.Population(config)
    # print the progress of the algorithm to the window
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    # run for up to 50 generations
    winner = p.run(eval_genomes, 50)
    # show final stats
    print("\nBest genome:\n{!s}".format(winner))


# the file is being run as the main program
if __name__ == "__main__":
    # hold the directory of the current file
    local_dir = os.path.dirname(__file__)
    # path to the configuration file that defines the settings for the NEAT algorithm
    config_path = os.path.join(local_dir, "config_feedforward.txt")
    # starts the main loop of the game and runs the NEAT algorithm to train the neural network to play the game
    run(config_path)
