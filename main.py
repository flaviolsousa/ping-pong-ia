from curses.ascii import NUL
import pygame
import sys
import os
from pygame.locals import *
from pygame._sdl2.video import Window

from classes.Game import Game

# Set up pygame
pygame.init()
clock = pygame.time.Clock()


# Set up the window
windowSurface = pygame.display.set_mode(
    (640, 480), HWSURFACE | DOUBLEBUF | RESIZABLE)

window = Window.from_display_module()
window.position = (0, 0)

game = Game(windowSurface)

# Run the game loop
while True:
  clock.tick(60)
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      sys.exit()
    elif event.type == VIDEORESIZE:
      screen = pygame.display.set_mode(
          event.size, HWSURFACE | DOUBLEBUF | RESIZABLE)
      pygame.display.flip()
  game.draw()
