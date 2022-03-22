from turtle import position
import pygame


class Player:

  COLOR_PLAYERS = (255, 255, 255)
  STEP = 2
  PLAYERS_CONFIGS = [
      {
          'position': 25,
          'keys': [pygame.K_a, pygame.K_z]
      },
      {
          'position': 75,
          'keys': [pygame.K_UP, pygame.K_DOWN]
      }
  ]

  def __init__(self, game, side):
    self.game = game
    self.side = side
    self.config = self.PLAYERS_CONFIGS[side-1]
    self.move = 0
    self.size = 20
    self.position = self.config['position'] - self.size/2
    self.points = 0

  def draw(self):
    keys = pygame.key.get_pressed()

    self.position += (keys[self.config['keys'][1]] -
                      keys[self.config['keys'][0]]) * self.STEP

    self.position = min(max(0, self.position), 100 - self.size)

    (w, h, uw, uh) = self.game.scale
    self.pw = uw if self.side == 1 else w-uw*2

    pygame.draw.rect(self.game.windowSurface, self.COLOR_PLAYERS,
                     pygame.Rect(self.pw, uh*self.position, uw, uh*self.size))
