from typing import Dict
import pygame

from classes.PlayerHuman import PlayerHuman
from classes.PlayerIA import PlayerIA
from classes.Ball import Ball


class Game:

  COLOR_CENTER_LINE = (255, 255, 255)
  COLOR_POINTS = (255, 255, 255)

  def __init__(self, windowSurface):
    self.player1 = PlayerIA(self, 1)
    self.player2 = PlayerHuman(self, 2)
    # self.player2 = PlayerIA(self, 2)
    self.ball = Ball(self)
    self.commands = {
        'player1': {
            'up': True,
            'down': False
        },
        'player2': {
            'up': True,
            'down': False
        }
    }
    self.windowSurface = windowSurface

  def __drawPoints(self):
    (w, h, uw, uh) = self.scale
    font = pygame.font.Font('Retro Gaming.ttf', int(w/25))
    # Points
    points1 = font.render(str(self.player1.points), True, self.COLOR_POINTS)
    points1Rect = points1.get_rect()
    points1Rect.topright = (w/2-uw*2, uh)
    self.windowSurface.blit(points1, points1Rect)

    points2 = font.render(str(self.player2.points), True, self.COLOR_POINTS)
    points2Rect = points2.get_rect()
    points2Rect.topleft = (w/2+uw*2, uh)
    self.windowSurface.blit(points2, points2Rect)

  def doStep(self):
    keys = pygame.key.get_pressed()

    self.commands['player1']['up'] = keys[pygame.K_a]
    self.commands['player1']['down'] = keys[pygame.K_z]
    self.commands['player2']['up'] = keys[pygame.K_UP]
    self.commands['player2']['down'] = keys[pygame.K_DOWN]

    w, h = pygame.display.get_surface().get_size()
    uw = w/100
    uh = h/100
    self.scale = (w, h, uw, uh)

    self.windowSurface.fill(0)

    # center line
    pygame.draw.line(self.windowSurface,
                     self.COLOR_CENTER_LINE, (w/2, 0), (w/2, h))

    self.player1.doStep()
    self.player2.doStep()
    self.ball.doStep()
    self.__drawPoints()

    # ball
    # pygame.draw.circle(self.windowSurface, self.COLOR_BALL,
    #                    (uw*70, uh*35), uw)

    pygame.display.flip()
