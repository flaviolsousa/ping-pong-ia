import random

from classes.PlayerHuman import PlayerHuman


class PlayerAI (PlayerHuman):

  STEP = 1
  NAME = "Artificial Intelligence"

  def __init__(self, game, side):
    PlayerHuman.__init__(self, game, side)

  def move(self):
    # (w, h, uw, uh) = self.game.scale
    # factor = random.randint(0, 9)

    safeAreaStart = self.position + self.size/10
    safeAreaEnd = safeAreaStart + self.size/10*8
    pName = self.config['name']

    if (pName == "player1" and self.game.ball.velX < 0) or (pName == "player2" and self.game.ball.velX > 0):
      self.game.commands[pName]['up'] = self.game.ball.posY < safeAreaStart
      self.game.commands[pName]['down'] = self.game.ball.posY > safeAreaEnd
    super().move()
