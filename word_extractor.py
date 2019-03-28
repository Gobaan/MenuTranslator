import pickle
import math
import statistics
from shapely.geometry.polygon import Polygon
import logging

class Word(object):
  def __init__(self, word):
    self.word = word['description']
    self.poly = [vertex for vertex in word['bounds']]
    self.bounds = Polygon(self.poly)
    self.projection = None
    x_bounds = [vertex[0] for vertex in self.poly]
    y_bounds = [vertex[1] for vertex in self.poly]
    self.x_bounds = min(x_bounds), max(x_bounds)
    self.y_bounds = min(y_bounds), max(y_bounds)

  def __calculate(self, fn):
    return (fn(self.poly[0], self.poly[1]) + fn(self.poly[3], self.poly[2])) / 2
  	
  def slant(self):
    # 0   1
    # 3   2
    def slope(v1, v2):
      return math.atan2(v2[1] - v1[1], v2[0] - v1[0])

    return self.__calculate(slope)

  def length(self):
    def line_length(v1, v2): 	
      def square(index):
      	return (v1[index] - v2[index]) *  (v1[index] - v2[index])
      return math.sqrt(square(0) + square(1))
    return self.__calculate(line_length)
  

  def __repr__(self):
    return f'Word({self.word}, {self.poly})'

  def is_money(self):
    money_characters = '1234567890$$€¥¢kK.RM'
    return sum(True for character in self.word if character in money_characters) / len(self.word) > 0.5

  def is_same_height(self, other):
      # test on food carts
      # fix slants
    def intersects(range1, range2):
      return (range1[0] <= range2[0] <= range1[1]) or (range2[0] <= range1[0] <= range2[1])
    def overlap(range1, range2):
      if not intersects(range1, range2):
        return 0.0
      len1 = range1[1] - range1[0]
      len2 = range2[1] - range2[0]
      start = statistics.median([range1[0], range2[0], range2[1]])
      end = statistics.median([range1[1], range2[0], range2[1]])
      return abs(end - start) / min(len1, len2)
    return overlap(self.y_bounds, other.y_bounds) > 0.5

  def precedes(self, other, length):
    self.__create_projection(length)
    return self.projection.intersects(other.bounds)

  def __create_projection(self, length):
    def project(x, y):
      theta = self.slant()
      return x + math.cos(theta) * length, y + math.sin(theta) * length

    if not self.projection:
      self.projection = Polygon([self.poly[1], project(*(self.poly[1])), project(*(self.poly[2])), self.poly[2]])


class Name(object):
  def __init__(self, words):
    self.words = words
    self.x_bounds = min(min(word.x_bounds) for word in words), max(max(word.x_bounds) for word in words)
    self.y_bounds = min(min(word.y_bounds) for word in words), max(max(word.y_bounds) for word in words)
 
  def __str__(self):
    name = ' '.join(word.word for word in self.words if not word.is_money())
    return f'{name}'

  def __repr__(self):
    return f'Food({str(self)}, X:{self.x_bounds}, Y:{self.y_bounds})'

  def encode(self, encoding):
      return str(self)

def get_bounds(names):
    x_bound = max(max(name.x_bounds) for name in names)
    y_bound = max(max(name.y_bounds) for name in names)
    return (x_bound, y_bound)

def get_theta(words):
    return sum(word.slant() for word in words) / len(words)

def get_names(text):
  #x_names = sorted(words, key=lambda word: word.x_bounds[0])
  # word_length = max(word.x_bounds[1] - word.x_bounds[0] for word in words)
  words = [Word(word) for word in text]
  lengths = sorted(word.length() for word in words)
  print (lengths)
  decile_length = lengths[int(len(lengths)*0.9)]
  while words:
    current = [words.pop(0)]
    for name in list(words):
        if current[-1].precedes(name, decile_length):
            current += [name]
            words.remove(name)
    output = Name(current)
    if str(output):
      yield output


if __name__ == '__main__':
  with open('menu.pickle', 'rb') as fp:
    ocr_json = pickle.load(fp)
  text = ocr_json[1:]
  print (ocr_json)
  words = [Word(word) for word in text]
  print (words[0])
  max_length = max(word.length() for word in words) 
  print (max_length)
  
  for name in get_names(text):
    if str(name):
      print('full', name)

