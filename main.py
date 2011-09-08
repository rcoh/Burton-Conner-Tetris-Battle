from time import sleep, time
import random
import sys
from renderer import *
from ddrinput import DdrInput
from ddrinput import DIRECTIONS
import pygame
import util
import colorsys
#import figure_builder

LETTER_WIDTH = 6

class Animation:

  def __init__(self):
    self.gui = [PygameRenderer(), LedRenderer()]
    self.letters = self.create_letter_dict()
    self.base = {}
    self.animate()

  def fill_background(self,dictionary,color):
    for x in range(20):
      for y in range(20):
        if (x,y) not in dictionary:
          dictionary[(x,y)] = color
    
  def sun(self):
    sun = self.get_letter_dict("sun","yellow")
    self.base = {}
    self.add_pic(self.base,sun,(2,0))

    h=(135.0/255)
    s=(224.0/255)
    v=(185.0/255)

    #(h,s,v)=(0.25, 0.5, 0.4)
    for i in range(40):
      v-=(10.0/255)
      v = max(v,0)
      r,g,b = colorsys.hsv_to_rgb(h, s, v)
      self.base = util.shift_dict(self.base, (0,1))
      #print r,b,g
      r = round(r*255)
      g = round(g*255)
      b = round(b*255)
      self.fill_background(self.base,(r,g,b))
      self.display(self.base)
      if i==0:
        sleep(1)
      elif i<22:
        sleep(.25)
      else:
        sleep(.2)

  def moon(self):
    moon = self.get_letter_dict("moon","yellow")
    stars = self.get_letter_dict("stars","gray")
    self.base = {}
    self.add_pic(self.base,moon,(3,20))
    for i in range(20):
      self.display(self.base)
      self.base = util.shift_dict(self.base, (0,-1))
      sleep(.3)
    sleep(.5)
    for i in range(50):
      the_moon = {}
      self.base = the_moon
      self.add_pic(the_moon,stars,(0,0))
      num_on = int(len(stars)*.6)
      print len(stars)
      stars_on = random.sample(stars,num_on)
      for key in stars_on:
        self.base[key] = "white"
      self.add_pic(the_moon,moon,(3,1))
      self.display(self.base)
      sleep(.3)
      
    self.base = {}
    on_stars = self.get_letter_dict("stars","gray")
    self.add_pic(self.base,moon,(3,1))
    self.add_pic(self.base,on_stars,(0,0))
    for i in range(20):
      self.display(self.base)
      self.base = util.shift_dict(self.base, (0,-1))
      sleep(.3)

  def scroll_text(self, text):
    word_dict = {}
    offset_x = 0
    for letter in text:
      letter_dict = self.get_letter_dict(letter, "white")
      word_dict = util.compose_dicts(word_dict, letter_dict, (offset_x, 0))
      offset_x += self.get_letter_width(letter) 
    self.base = word_dict
    for i in range(50):
      self.display(self.base)
      self.base = util.shift_dict(self.base, (-1, 0))
      sleep(.3)

  def get_letter_width(self, letter):
    if letter == "I":
      return 2
    else:
      return 6
  def animate(self):
    self.sun()
    self.moon()
    self.scroll_text("GOODNIGHT ALLY")
  
  def display(self,d):
    [gui.render_game(d) for gui in self.gui]

  def create_letter_dict(self):
    d = {}
    d["moon"] = [(5,0),(6,0),(7,0),(8,0),(3,1),(4,1),(5,1),(6,1),
           (2,2),(3,2),(4,2),(1,3),(2,3),(3,3),(1,4),(2,4),(3,4),
           (0,5),(1,5),(2,5),(3,5),
           (5,10),(6,10),(7,10),(8,10),(3,9),(4,9),(5,9),(6,9),
           (2,8),(3,8),(4,8),(1,7),(2,7),(3,7),(1,6),(2,6),(3,6)]

    d["sun"] = self.make_sun()
    d["stars"] = self.make_stars()
    d["I"] = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)]
    d[" "] = {}
    return d

  def make_stars(self):
    stars = []
    for i in range(40):
      stars += [(1,2),(1,12),(3,17),(3,9),
                (5,0),(5,14),(7,12),(7,17),
                (9,3),(9,6),(11,3),(11,13),
                (13,9),(13,16),(15,1),(15,13),
                (17,6),(17,16),(19,3),(19,9)
      ]
    return stars    
    
  def make_sun(self):
    final = []
    full = []
    half = []
    quad = [(0,0),(1,0),(2,0),(4,0),(5,0),(6,0),(0,1),(1,1),(2,1),
       (0,2),(1,2),(3,3),(4,3),(0,4),(4,4),(5,4),(0,5),(5,5),
       (0,6),(6,5),(6,6),(7,0),(0,7)]
    half = quad[:]
    for (x,y) in quad:
      half += [(-y-1,x)]
    full = half[:]
    for (x,y) in half:
      full += [(x,-y-1)]
    for (x,y) in full:
      final += [(x+8,y+8)]
    #print final
    return final
    
    

  def create_picture_dict(self): #multi-color pics...
    d = {}
    

  def get_letter_dict(self,letter, color):
    if not letter in self.letters:
      letter = letter.lower()
      try:
        letter_array = figure_builder.dict_from_image_file('img/' + letter + '.png', (5,5)) 
      except IOError:
        return {}
    else:
      letter_array = self.letters[letter]
    d={}
    for key in letter_array:
      d[key] = color
    return d
    
  def add_pic(self,start_dict,new_pic,top_left):
    for (x,y) in new_pic:
      start_dict[x+top_left[0],y+top_left[1]]=new_pic[(x,y)]

class TextAnimation:
  def __init__(self, text):
    super(TextAnimation, self).__init__()
    self.base = {}
    text_width = 0
    for letter in text:
      letter_dict = get_dict(letter) ###replace
      util.compose_dicts(self.base, letter, LETTER_WIDTH)
      text_width += LETTER_WIDTH
  
    self.base = util.shift_dict(self.base, (-text_width, 0))
if __name__ == "__main__":
  animation = Animation()
