import pygame
from pygame.locals import *


def main():
  pygame.init()
  screen = pygame.display.set_mode(
      (200, 200), HWSURFACE | DOUBLEBUF | RESIZABLE)
  fake_screen = screen.copy()
  pic = pygame.surface.Surface((50, 50))
  pic.fill((255, 100, 200))

  while True:
    for event in pygame.event.get():
      if event.type == QUIT:
        pygame.display.quit()
      elif event.type == VIDEORESIZE:
        screen = pygame.display.set_mode(
            event.size, HWSURFACE | DOUBLEBUF | RESIZABLE)

    fake_screen.fill('black')
    fake_screen.blit(pic, (100, 100))
    screen.blit(pygame.transform.scale(
        fake_screen, screen.get_rect().size), (0, 0))
    pygame.display.flip()


main()
