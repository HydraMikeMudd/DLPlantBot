
# DLPlant Discord Bot

## Intro

This bot is intended to explore creating fractal plants in the context of discord. As it currently stands, this bot can create random plants using L Systems and send these plants as images back to users. The application consists of two main scripts: main.py and grow_trees.py.

## main.py

This is the script that defines the commands for the bot and provides the main functionality of the bot. It interacts with a database to check if a user plant exists, create new user records, check if a tree file exists, etc.. This script does not grow the plants or create the plant images however.

## grow_trees.py

This is the script that produces the plant images as well as grow any plants that are flagged as such in the database. This script runs about every 60 seconds.

### TODO:

1. Test new L Systems and find upper limit for iterations (needed to ensure sufficient response times)
2. Plan progression systems (timed based, more game like, linear/more log like)
3. Visual adjustments to plants (color, angles, etc)
