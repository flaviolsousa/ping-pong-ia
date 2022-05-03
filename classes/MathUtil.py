class Point:
  def __init__(self, x, y):
    self.x = x
    self.y = y

  def __str__(self):
    return "[" + "%.2f" % self.x + ", " + "%.2f" % self.y + "]"


class Line:
  def __init__(self, p1, p2):
    self.p1 = p1
    self.p2 = p2

  def __str__(self):
    return "[" + str(self.p1) + ", " + str(self.p2) + "]"


def ccw(a, b, c):
  return (c.y-a.y)*(b.x-a.x) > (b.y-a.y)*(c.x-a.x)


def intersect(l1, l2):
  return ccw(l1.p1, l2.p1, l2.p2) != ccw(l1.p2, l2.p1, l2.p2) and ccw(l1.p1, l1.p2, l2.p1) != ccw(l1.p1, l1.p2, l2.p2)
