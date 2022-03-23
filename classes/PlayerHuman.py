import pygame


class PlayerHuman:

  COLOR_PLAYERS = (255, 255, 255)
  STEP = 2
  PLAYERS_CONFIGS = [
      {
          'position': 25,
          'name': "player1"
      },
      {
          'position': 75,
          'name': "player2"
      }
  ]

  def __init__(self, game, side):
    self.game = game
    self.side = side
    self.config = self.PLAYERS_CONFIGS[side-1]
    self.size = 20
    self.position = self.config['position'] - self.size/2
    self.points = 0

  def move(self):
    self.position += (self.game.commands[self.config['name']]['down'] -
                      self.game.commands[self.config['name']]['up']) * self.STEP

  def doStep(self):
    self.move()
    self.position = min(max(0, self.position), 100 - self.size)

    (w, h, uw, uh) = self.game.scale
    self.pw = uw if self.side == 1 else w-uw*2

    pygame.draw.rect(self.game.windowSurface, self.COLOR_PLAYERS,
                     pygame.Rect(self.pw, uh*self.position, uw, uh*self.size))
