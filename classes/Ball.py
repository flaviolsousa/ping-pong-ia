from turtle import position
from numpy import absolute
import pygame
import random
from classes.MathUtil import Point, Line, intersect


class Ball:

  COLOR_BALL = (255, 255, 255)

  def __init__(self, game):
    self.game = game
    self.restart(1)

  def restart(self, lastWinner):
    self.finish = False
    self.posX = 50
    self.posY = 35
    self.setVelY(random.random()/2)

    self.booster = 1
    if lastWinner == 2:
      self.velX *= -1

  def setVelY(self, velY):
    self.velY = velY
    self.velX = 1-abs(velY)

  def move(self):
    (w, h, uw, uh) = self.game.scale

    newX = self.posX + self.velX * self.booster
    newY = self.posY + self.velY * self.booster
    ballL = Line(Point(newX, newY),
                 Point(self.posX, self.posY))

    if not self.finish:
      player = self.game.player2 if self.velX > 0 else self.game.player1
      enemyPlayer = self.game.player1 if self.velX > 0 else self.game.player2
      playerL = Line(Point(player.bumpLine, player.position - 1),
                     Point(player.bumpLine, player.position + player.size + 1))
      self.bumped = intersect(ballL, playerL)

      if newY < 1:
        self.posY = 2 - newY
        self.velY *= -1
      elif newY > 99:
        self.posY = newY - 2
        self.velY *= -1
      else:
        self.posY = newY

      if self.bumped:
        self.velX *= -1
        self.booster += 0.1
        colisionFactor = self.posY-player.position
        self.setVelY(colisionFactor/player.size-0.5)
        if player.side == 1:
          self.posX = newX + (player.bumpLine - newX)
        else:
          self.posX = newX - (newX - player.bumpLine)
          self.velX *= -1
      elif (player.side == 1 and newX < player.bumpLine) or (player.side == 2 and newX > player.bumpLine):
        self.finish = True
        self.lastWinner = enemyPlayer.side
        enemyPlayer.points += 1
      else:
        self.posX = newX

    else:
      if not -1 <= self.posX <= 101:
        self.restart(self.lastWinner)
      else:
        self.posX += self.velX
        self.posY += self.velY

  def doStep(self):
    (w, h, uw, uh) = self.game.scale

    self.move()

    pygame.draw.circle(self.game.windowSurface, self.COLOR_BALL,
                       (uw*self.posX, uh*self.posY), uw)
