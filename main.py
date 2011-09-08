from time import sleep, time
import random
import sys
from renderer import *
from ddrinput import DdrInput
from ddrinput import DIRECTIONS
import pygame
import util

class Animation:

    def __init__(self):
        self.gui = [PygameRenderer(), LedRenderer()] 
        d={}
        d[1,1] = "yellow"
        self.base = d
        self.animate()

    def animate(self):
      while 1:
        self.display(self.base)
        self.base = util.shift_dict(self.base, (1,1))
        sleep(.3)
  

    def display(self,d):
        [gui.render_game(d) for gui in self.gui]
        

if __name__ == "__main__":
    animation = Animation()
