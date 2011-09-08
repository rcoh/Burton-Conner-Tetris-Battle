from time import sleep, time
import random
import sys
from renderer import *
from ddrinput import DdrInput
from ddrinput import DIRECTIONS
import pygame
import util

LETTER_WIDTH = 6

class Animation:

    def __init__(self):
        self.gui = [PygameRenderer(), LedRenderer()] 
     
    def start_animation(self):
      while 1:
        self.display(self.base)
        self.base = util.shift_dict(self.base, (1,1))
        sleep(.3)
  

    def display(self,d):
        [gui.render_game(d) for gui in self.gui]

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
