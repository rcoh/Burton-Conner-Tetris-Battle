from time import sleep, time
import random
import sys
from renderer import *
from tetris_shape import *
from ddrinput import DdrInput
from ddrinput import DIRECTIONS
import pygame


class Animation:

    def __init__(self):
        self.gui = [PygameRenderer(), LedRenderer()] 
        self.animate()

    def animate(self):
        d={}
        d[1,1] = "yellow"
        self.display(d)

    def display(self,d):
        [gui.render_game(d) for gui in self.gui]

    def create_letter_dict(self):
        d = {}
        d["A"] = [(0,1),(0,2),(0,3),(0,4),(1,0),(2,0),(3,0),(4,1),(4,2),(4,3),(4,4)]
        

if __name__ == "__main__":
    animation = Animation()
