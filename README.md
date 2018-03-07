# Overview

Uses a very simple [Q-learning](https://en.wikipedia.org/wiki/Q-learning) algorithm to play Flappy Bird, implemented as a table.

# Running

Run in Python 3

`python3 flappy.py`

If it does not have the file `qvalues.json` it will create a new file with all values initialized as 0. It updates the file every 25 games, so you can turn off the application and resume later if you want to train for a long time.

Haveily based on the project made by [sarvagyavanish](https://sarvagyavaish.github.io/FlappyBirdRL/) and [this](https://github.com/chncyhn/flappybird-qlearning-bot) by chncyhn (who used the high death flag) and runs on [this](https://github.com/sourabhv/FlapPyBird) Flappy Bird clone in Python.