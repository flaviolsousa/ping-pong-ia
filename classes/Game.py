from typing import Dict
import pygame

from classes.Ball import Ball
from config import FRAMES_PER_SECOND_DEFAULT


class Game:

  COLOR_CENTER_LINE = (255, 255, 255)
  COLOR_POINTS = (255, 255, 255)
  COLOR_NAME = (255, 255, 255)
  COLOR_FPS = (255, 255, 255)

  def __init__(self, windowSurface, clock):
    self.framesPerSecond = FRAMES_PER_SECOND_DEFAULT
    self.ball = Ball(self)
    self.commands = {
        'player1': {
            'up': False,
            'down': False
        },
        'player2': {
            'up': False,
            'down': False
        }
    }
    self.windowSurface = windowSurface
    self.clock = clock

  def __drawFPS(self):
    (w, h, uw, uh) = self.scale
    fontFPS = pygame.font.Font('Retro Gaming.ttf', int(w/50))
    text = fontFPS.render(
        str(round(self.clock.get_fps())) + ' fps', True, self.COLOR_FPS)
    self.windowSurface.blit(text, (uw, uh*95))

  def __drawPoints(self):
    (w, h, uw, uh) = self.scale
    fontPoints = pygame.font.Font('Retro Gaming.ttf', int(w/25))
    fontName = pygame.font.Font('Retro Gaming.ttf', int(w/50))
    # Points
    points1 = fontPoints.render(
        str(self.player1.points), True, self.COLOR_POINTS)
    points1Rect = points1.get_rect()
    points1Rect.topright = (w/2-uw*2, uh*4)
    self.windowSurface.blit(points1, points1Rect)

    points2 = fontPoints.render(
        str(self.player2.points), True, self.COLOR_POINTS)
    points2Rect = points2.get_rect()
    points2Rect.topleft = (w/2+uw*2, uh*4)
    self.windowSurface.blit(points2, points2Rect)

    # name
    name1 = fontName.render(str(self.player1.NAME), True, self.COLOR_NAME)
    name1Rect = name1.get_rect()
    name1Rect.topright = (w/2-uw*2, uh)
    self.windowSurface.blit(name1, name1Rect)

    name2 = fontName.render(str(self.player2.NAME), True, self.COLOR_NAME)
    name2Rect = name2.get_rect()
    name2Rect.topleft = (w/2+uw*2, uh)
    self.windowSurface.blit(name2, name2Rect)

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
    self.player1.doLearn()
    self.player2.doLearn()
    self.__drawFPS()
    self.__drawPoints()

    # ball
    # pygame.draw.circle(self.windowSurface, self.COLOR_BALL,
    #                    (uw*70, uh*35), uw)

    pygame.display.flip()
