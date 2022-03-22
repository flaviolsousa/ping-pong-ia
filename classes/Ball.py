from turtle import position
from numpy import absolute
import pygame
import random


class Ball:

  COLOR_BALL = (255, 255, 255)

  def __init__(self, game, player1, player2):
    self.game = game
    self.player1 = player1
    self.player2 = player2
    self.restart(1)

  def restart(self, lastWinner):
    self.finish = False
    self.posX = 50
    self.posY = 35
    self.setVelY(random.random()/2)
    self.velY *= -1 if random.choice([True, False]) else 1
    if lastWinner == 2:
      self.velX *= -1

  def setVelY(self, velY):
    self.velY = velY
    self.velX = 1-abs(velY)

  def move(self):
    (w, h, uw, uh) = self.game.scale
    radius = uw

    self.posX += self.velX
    self.posY += self.velY

    if (self.posY + 2 > 100):
      self.velY *= -1
    if (self.posY - 2 < 0):
      self.velY *= -1

    if not self.finish:
      if uw*(self.posX+1) > self.player2.pw:
        colisionFactor = self.posY-self.player2.position
        if 0 <= colisionFactor <= self.player2.size:
          self.setVelY(colisionFactor/self.player2.size-0.5)
          self.velX *= -1
        else:
          self.finish = True
          self.lastWinner = 1
          self.player1.points += 1

      if uw*(self.posX-1) < self.player1.pw:
        colisionFactor = self.posY-self.player1.position
        if 0 <= colisionFactor <= self.player1.size:
          self.setVelY(colisionFactor/self.player1.size-0.5)
        else:
          self.finish = True
          self.lastWinner = 2
          self.player2.points += 1
    else:
      if not -1 <= self.posX <= 101:
        self.restart(self.lastWinner)

  def draw(self):
    (w, h, uw, uh) = self.game.scale

    self.move()

    pygame.draw.circle(self.game.windowSurface, self.COLOR_BALL,
                       (uw*self.posX, uh*self.posY), uw)
