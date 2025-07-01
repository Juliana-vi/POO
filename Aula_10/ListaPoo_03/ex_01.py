import math
class Retângulo:
  def __init__(self, b, h):
    self.__b = 0
    self.__h = 0
    self.set_base(b)
    self.set_altura(h)
  def set_base(self, v):
    if v >= 0: self.__b = v
    else: raise ValueError()
  def set_altura(self, v):
    if v >= 0: self.__h = v
    else: raise ValueError()

  def get_base(self):
    return self.__b
  def get_altura(self):
    return self.__h
  def calc_area(self):
    return self.__b * self.__h
  def calc_diagonal(self):
    return math.sqrt((self._b) **2 + (self._h) **2)
  def __str__(self):
    return f"Base = {self.__b} - Altura = {self.__h} - Area = {self.__b * self.__h} - Diagonal = {math.sqrt((self._b) **2 + (self._h) **2)}"
  print(f"Área = {calc_area} - Diagonal = {calc_diagonal}