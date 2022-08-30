import pygame


class PlayerHuman:

  NAME = "Human"
  COLOR_PLAYERS = (255, 255, 255)
  STEP = 1.5
  PLAYERS_CONFIGS = [
      {
          'position': 25,
          'name': "player1",
          'posX': 1,
          'bumpLine': 2
      },
      {
          'position': 75,
          'name': "player2",
          'posX': 98,
          'bumpLine': 98
      },
  ]

  def __init__(self, game, side):
    self.game = game
    self.side = side
    self.config = self.PLAYERS_CONFIGS[side-1]
    self.size = 20
    self.position = self.config['position'] - self.size/2
    self.posX = self.config['posX']
    self.bumpLine = self.config['bumpLine']
    self.points = 0
    setattr(game, self.config['name'], self)

  def move(self):
    pName = self.config['name']
    self.position += (self.game.commands[pName]['down'] -
                      self.game.commands[pName]['up']) * self.STEP

  def doStep(self):
    self.move()
    self.position = min(max(0, self.position), 100 - self.size)

    (w, h, uw, uh) = self.game.scale
    self.pw = self.posX*uw
    self.ph = uh*self.position
    self.sw = uh
    self.sh = uh*self.size

    pygame.draw.rect(self.game.windowSurface, self.COLOR_PLAYERS,
                     pygame.Rect(self.pw, self.ph, self.sw, self.sh))

  def doLearn(self):
    self.learn()

  def learn(self):
    pass
