import random
from enum import IntEnum

from classes.PlayerHuman import PlayerHuman

import torch
import numpy as np
import pygame
from collections import deque
from classes.model.model import Linear_QNet, QTrainer
from classes.model.helper import plot
from config import TRAINING, INITIAL_RECORD, LR, GAMMA, MAX_LOSSES, EXPLORATION_GAMES


class Commands(IntEnum):
  STAY = 0
  UP = 1
  DOWN = 2


class States(IntEnum):
  BALL_DISTANCE_X = 0
  BALL_DISTANCE_Y = 1
  BALL_VELOCITY_X = 2
  BALL_VELOCITY_Y = 3
  PLAYER_POSITION = 4
  ENEMY_POSITION = 5


DRAW_STATE = False

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
# LR = 0.001
# LR = 0.0001

INPUT_LAYER = 6  # NN input layer size
# HIDDEN_LAYER = 256  # NN hidden layer size
HIDDEN_LAYER = INPUT_LAYER * 20  # NN hidden layer size


class PlayerNN (PlayerHuman):
  STEP = PlayerHuman.STEP / 2

  def __init__(self, game, side):
    PlayerHuman.__init__(self, game, side)
    self.training = TRAINING
    if self.training:
      self.watching = False
      self.record = INITIAL_RECORD
      self.totalRewards = 0
      self.plotScores = []
      self.plotBumps = []
      self.restart()

      self.nGames = 0
      self.epsilon = 0  # randomness
      self.gamma = GAMMA  # discount rate
      self.memory = deque(maxlen=MAX_MEMORY)  # popleft()

    self.model = Linear_QNet(INPUT_LAYER, HIDDEN_LAYER, len(Commands))
    if self.training:
      self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

  def drawState(self):
    if hasattr(self, 'stateOld'):
      (w, _, uw, uh) = self.game.scale

      font = pygame.font.Font('Retro Gaming.ttf', int(uw*2))
      for i, value in enumerate(self.stateOld):
        label = font.render(str("%.2f" % value), True, self.game.COLOR_POINTS)
        labelRect = label.get_rect()
        labelRect.topleft = (w/2+uw*4, uh*20 + (uh*4*i))
        self.game.windowSurface.blit(label, labelRect)

  def remember(self, state, action, reward, next_state, done):
    self.memory.append((state, action, reward, next_state, done))

  def getAction(self, state):
      # random moves: tradeoff exploration / exploitation
    finalMove = np.zeros(len(Commands))
    if self.training:
      self.epsilon = EXPLORATION_GAMES - self.nGames
    if self.training and random.randint(0, EXPLORATION_GAMES*2) < self.epsilon:
      # if self.training and random.randint(0, 100) < 50:
      self.exploration = self.epsilon/(EXPLORATION_GAMES*2)
      move = random.randint(0, len(Commands) - 1)
      # move = Directions.UP if state[States.BALL_DISTANCE_Y] > 0 else Directions.DOWN
    else:
      stateTensor = torch.tensor(state, dtype=torch.float)
      prediction = self.model(stateTensor)
      move = torch.argmax(prediction).item()
    finalMove[move] = 1
    return finalMove

  def move(self):
    if not self.game.ball.finish:
      self.watching = True
    self.stateOld = self.getState()
    if DRAW_STATE:
      self.drawState()
    # print(self.side, ":", inputs)

    self.lastMove = self.getAction(self.stateOld)

    pName = self.config['name']
    self.game.commands[pName]['up'] = bool(self.lastMove[Commands.UP])
    self.game.commands[pName]['down'] = bool(self.lastMove[Commands.DOWN])
    super().move()

  def learn(self):
    if (not self.watching):
      return
    if not self.training:
      return

    self.stateNew = self.getState()

    if (not self.game.ball.finish):
      if self.game.ball.bumped:
        self.amountBumps += 1
        reward = 25
      else:
        reward = 0
    else:
      self.watching = False
      if (self.game.ball.lastWinner == self.side):
        self.amountWin += 1
        reward = 50
      else:
        reward = -100
        self.amountLost += 1
    done = self.amountLost >= MAX_LOSSES
    self.totalRewards += reward

    # print("%.2f" % self.stateNew[1])

    self.trainShortMemory(self.stateOld, self.lastMove,
                          reward, self.stateNew, not self.watching)
    self.remember(self.stateOld, self.lastMove, reward, self.stateNew, done)

    if(done):
      print('Epic:', self.nGames,
            '  Score:', self.amountWin,
            '  exploration:', '%.2f' % self.exploration,
            '  Record:', self.record,
            '  Rewards:', self.totalRewards)

      if self.totalRewards > self.record:
        self.record = self.totalRewards
        self.model.save()
        print("> Model Saved")

      self.plotScores.append(self.amountWin)
      self.plotBumps.append(self.amountBumps)

      self.restart()
      self.nGames += 1
      self.game.player1.points = 0
      self.game.player2.points = 0
      self.trainLongMemory()

      plot(self.plotScores, self.plotBumps)

  def restart(self):
    self.amountWin = 0
    self.amountLost = 0
    self.amountBumps = 0
    self.totalRewards = 0

  def getState(self):
    ball = self.game.ball
    if self.side == 2:
      player = self.game.player2
      enemyPlayer = self.game.player1
      factor = 1
    else:
      player = self.game.player1
      enemyPlayer = self.game.player2
      factor = -1

    # States: BALL_DISTANCE_X, BALL_DISTANCE_Y, BALL_VELOCITY_X, BALL_VELOCITY_Y, PLAYER_POSITION, ENEMY_POSITION
    return [((player.bumpLine - ball.posX) * factor) / 100, (player.position - ball.posY) / 100, ball.velX * factor, ball.velY, player.position/100, enemyPlayer.position/100]

  def trainShortMemory(self, state, action, reward, next_state, done):
    self.trainer.train_step(state, action, reward, next_state, done)

  def trainLongMemory(self):
    if len(self.memory) > BATCH_SIZE:
      miniSample = random.sample(self.memory, BATCH_SIZE)  # list of tuples
    else:
      miniSample = self.memory

    states, actions, rewards, nextStates, dones = zip(*miniSample)
    self.trainer.train_step(states, actions, rewards, nextStates, dones)
