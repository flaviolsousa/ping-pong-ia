
import matplotlib.pyplot as plt
from IPython import display

plt.ion()


def plot(scores, bumps):
  display.clear_output(wait=True)
  display.display(plt.gcf())
  plt.clf()
  plt.title('Training...')
  plt.xlabel('Number of Games')
  plt.ylabel('Score')
  plt.plot(scores)
  plt.plot(bumps)
  plt.ylim(ymin=0)
  plt.text(len(scores)-1, scores[-1], str(scores[-1]))
  plt.text(len(bumps)-1, bumps[-1], str(bumps[-1]))
  plt.show(block=False)
  plt.pause(.1)
