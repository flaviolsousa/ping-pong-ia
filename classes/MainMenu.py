
from classes.PlayerHuman import PlayerHuman
from classes.PlayerAI import PlayerAI
from classes.PlayerNN import PlayerNN

import pygame


class MainMenu:

  COLOR = (255, 255, 255)

  def __init__(self, windowSurface, game):

    self.optionsPlayer1 = [PlayerAI.NAME, PlayerNN.NAME, PlayerHuman.NAME]
    self.optionsPlayer2 = [PlayerAI.NAME, PlayerNN.NAME, PlayerHuman.NAME,
                           PlayerNN.NAME + " Training"]

    self.windowSurface = windowSurface
    self.game = game

    self.selected1 = 0
    self.selected2 = 1

    self.player1 = None
    self.player2 = None

  def createPlayer(self, i, side):
    if i == 0:
      return PlayerAI(self.game, side)
    elif i == 1:
      return PlayerNN(self.game, side, False)
    elif i == 2:
      return PlayerHuman(self.game, side)
    elif i == 3:
      return PlayerNN(self.game, side, True)

  def doStep(self):
    w, h = pygame.display.get_surface().get_size()
    uw = w/100
    uh = h/100
    self.scale = (w, h, uw, uh)

    if self.player1 == None or self.player2 == None:
      self.processMenu()
      self.drawMenu()
      return False
    else:
      return True

  def processMenu(self):
    keys = pygame.key.get_pressed()

    self.finish = keys[pygame.K_KP_ENTER] or keys[pygame.K_RETURN]
    if self.finish:
      print("Selected")
      self.player1 = self.createPlayer(self.selected1, 1)
      self.player2 = self.createPlayer(self.selected2, 2)

    player1Up = keys[pygame.K_a] and not self.player1Up
    player1Down = keys[pygame.K_z] and not self.player1Down
    player2Up = keys[pygame.K_UP] and not self.player2Up
    player2Down = keys[pygame.K_DOWN] and not self.player2Down

    if player1Up:
      self.selected1 = max(0, self.selected1 - 1)
    elif player1Down:
      self.selected1 = min(len(self.optionsPlayer1)-1, self.selected1 + 1)

    if player2Up:
      self.selected2 = max(0, self.selected2 - 1)
    elif player2Down:
      self.selected2 = min(len(self.optionsPlayer2)-1, self.selected2 + 1)

    self.player1Up = keys[pygame.K_a]
    self.player1Down = keys[pygame.K_z]
    self.player2Up = keys[pygame.K_UP]
    self.player2Down = keys[pygame.K_DOWN]

  def drawMenu(self):
    self.windowSurface.fill(0)
    (w, h, uw, uh) = self.scale
    fontOptions = pygame.font.Font('Retro Gaming.ttf', int(w/50))
    fontChoosePlayer = pygame.font.Font('Retro Gaming.ttf', int(w/25))
    fontKeys = pygame.font.Font('Retro Gaming.ttf', int(w/50))

    optionsMarginTop = 40
    optionsLineHeight = 5

    # center line
    pygame.draw.line(self.windowSurface,
                     self.COLOR, (w/2, 0), (w/2, h))

    # Choose a player
    choosePlayer1 = fontChoosePlayer.render(
        "Choose a Player", True, self.COLOR)
    choosePlayer1Rect = choosePlayer1.get_rect()
    choosePlayer1Rect.topright = (w/2-uw*5, uh*2)
    self.windowSurface.blit(choosePlayer1, choosePlayer1Rect)

    choosePlayer2 = fontChoosePlayer.render(
        "Choose a Player", True, self.COLOR)
    choosePlayer2Rect = choosePlayer2.get_rect()
    choosePlayer2Rect.topleft = (w/2+uw*5, uh*2)
    self.windowSurface.blit(choosePlayer2, choosePlayer2Rect)

    # Keys
    keys1 = fontKeys.render("Keys: A or Z", True, self.COLOR)
    keys1Rect = keys1.get_rect()
    keys1Rect.topright = (w/2-uw*5, uh*10)
    self.windowSurface.blit(keys1, keys1Rect)

    keys2 = fontKeys.render("Keys: Arrows Up or Down", True, self.COLOR)
    keys2Rect = keys2.get_rect()
    keys2Rect.topleft = (w/2+uw*5, uh*10)
    self.windowSurface.blit(keys2, keys2Rect)

    # options
    for i, val in enumerate(self.optionsPlayer1):
      options1 = fontOptions.render(val, True, self.COLOR)
      options1Rect = options1.get_rect()
      options1Rect.topright = (
          w/2-uw*10, uh*optionsMarginTop+uh*optionsLineHeight*i)
      self.windowSurface.blit(options1, options1Rect)

    for i, val in enumerate(self.optionsPlayer2):
      options2 = fontOptions.render(val, True, self.COLOR)
      options2Rect = options2.get_rect()
      options2Rect.topleft = (
          w/2+uw*10, uh*optionsMarginTop+uh*optionsLineHeight*i)
      self.windowSurface.blit(options2, options2Rect)

    # bullet
    pygame.draw.circle(self.game.windowSurface, self.COLOR,
                       (w/2-uw*5, uh*(optionsMarginTop+1.5) + uh*optionsLineHeight*self.selected1), uw)
    pygame.draw.circle(self.game.windowSurface, self.COLOR,
                       (w/2+uw*5, uh*(optionsMarginTop+1.5) + uh*optionsLineHeight*self.selected2), uw)

    pygame.display.flip()
