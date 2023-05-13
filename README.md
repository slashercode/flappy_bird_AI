# Flappy Bird AI with NeuroEvolution of Augmenting Topologies (NEAT)

## Project Overview

This personal project is a Python implementation of an artificial intelligence (AI) that learns to play the popular game **Flappy Bird**. The AI is trained using the **_NeuroEvolution of Augmenting Topologies (NEAT)_** algorithm to evolve a neural network that controls the bird's movements.

## Requirements

The following packages are required for this project:

- Pygame
- OS
- Random
- Time
- NEAT-Python

It is recommended to install these packages using a package manager such as pip or conda. For example, to install these packages using pip, open a terminal or command prompt and run the following command:

    pip install pygame neat-python

**Note:** Some of these packages may have dependencies that need to be installed as well.

## Running the Flappy Bird AI

1.  Clone or download the project repository.
2.  Navigate to the project directory in your terminal.
3.  Run the following command:

        python flappy_bird_ai.py

This will start the game with the AI agent playing Flappy Bird. You can also adjust the NEAT algorithm's parameters by editing the **'config-feedforward.txt'** file.

## Project Workflow

There are three classes in the project, namely, **Bird**, **Pipe** and **Base**.

The class definition of a Bird object represents a Flappy Bird game character. The class has several constants (IMGS, MAX_ROTATION, ROT_VEL, ANIMATION_TIME) and methods (init(), jump(), move(), draw(), get_mask()) that define the behavior of the bird.

The class definition of a Pipe object represents a pipe object in the game. The class has several constants (GAP, VEL) and methods (init(), set_height(), move(), collide()) that define the behavior of the pipe.

The class definition of a Base object represents a moving base object in the game. The class has several constants (VEL, WIDTH, IMG) and methods (init(), move(), draw()) that define the behavior of the base.

The **blitRotateCenter()** function is useful for rotating and blitting images to the game window.

The **draw_window()** function draws the game window for the main game loop.
It clears the window by drawing the background image. It then draws the bird, pipes and base. It also displays the score, number of generations, and number of birds still alive on the window.

The **eval_genomes()** function implement the main game loop of the Flappy Bird game using the NEAT algorithm for AI.

The **run()** function runs the NEAT algorithm to train a neural network to play the game Flappy Bird. The NEAT (NeuroEvolution of Augmenting Topologies) algorithm is a genetic algorithm that evolves neural networks for various tasks. In this case, it is being used to train a neural network to play Flappy Bird.

## Acknowledgement

This project was inspired by the original Flappy Bird game created by Dong Nguyen and the NEAT-Python library created by CodeReclaimers.

## License

**NOT FOR COMMERCIAL USE**

_If you intend to use any of my code for commercial use please contact me and get my permission._

_If you intend to make money using any of my code please get my permission._
