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
        self.letters = self.create_letter_dict()
        self.base = {}
        self.start()

    def start(self):
        #d[1,1] = "yellow"
        A = self.get_letter_dict("A","yellow")
        L1 = self.get_letter_dict("L","orange")
        L2 = self.get_letter_dict("L","red")
        Y = self.get_letter_dict("Y","purple")
        self.add_pic(self.base,A,(0,0))
        self.add_pic(self.base,L1,(6,0))
        self.add_pic(self.base,L2,(11,0))
        self.add_pic(self.base,Y,(14,0))
        self.animate()

    def animate(self):
      while 1:
        self.display(self.base)
        self.base = util.shift_dict(self.base, (1,1))
        sleep(.3)
  
    def display(self,d):
        [gui.render_game(d) for gui in self.gui]

    def create_letter_dict(self):
        d = {}
        d["A"] = [(0,1),(0,2),(0,3),(0,4),(1,0),(2,0),(3,0),
                  (4,1),(4,2),(4,3),(4,4),(1,2),(2,2),(3,2)]
        d["L"] = [(0,0),(0,1),(0,2),(0,3),(0,4),
                  (1,4),(2,4),(3,4)]
        d["Y"] = [(0,0),(1,1),(2,2),(3,1),(4,0),(2,3),(2,4)]
                  
        return d

    def get_letter_dict(self,letter, color):
        d={}
        letter_array = self.letters[letter]
        for key in letter_array:
            d[key] = color
        return d
        
    def add_pic(self,start_dict,new_pic,top_left):
        for (x,y) in new_pic:
            start_dict[x+top_left[0],y+top_left[1]]=new_pic[(x,y)]

if __name__ == "__main__":
    animation = Animation()
