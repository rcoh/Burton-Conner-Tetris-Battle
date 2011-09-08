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
        self.animate()

    def animate(self):
        A = self.get_letter_dict("A","yellow")
        L1 = self.get_letter_dict("L","orange")
        L2 = self.get_letter_dict("L","red")
        Y = self.get_letter_dict("Y","purple")
        moon = self.get_letter_dict("moon","yellow")
        sun = self.get_letter_dict("sun","yellow")
        stars = self.get_letter_dict("stars","gray")
        """
        self.add_pic(self.base,A,(0,0))
        self.add_pic(self.base,L1,(6,0))
        self.add_pic(self.base,L2,(11,0))
        self.add_pic(self.base,Y,(14,0))
        """
    
        self.add_pic(self.base,sun,(2,0))

        self.display(self.base)
        sleep(1)
        for i in range(20):
            self.display(self.base)
            self.base = util.shift_dict(self.base, (0,1))
            sleep(.3)

        self.base = {}
        self.add_pic(self.base,moon,(3,20))
        for i in range(20):
            print "here"
            self.display(self.base)
            self.base = util.shift_dict(self.base, (0,-1))
            sleep(.3)
        
        for i in range(30):
            the_moon = {}
            self.base = the_moon
            self.add_pic(the_moon,stars,(0,0))
            stars_on = random.sample(stars,30)
            for key in stars_on:
                self.base[key] = "white"
            self.add_pic(the_moon,moon,(3,0))
            self.display(self.base)
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

        d["moon"] = [(5,0),(6,0),(7,0),(8,0),(3,1),(4,1),(5,1),(6,1),
                     (2,2),(3,2),(4,2),(1,3),(2,3),(3,3),(1,4),(2,4),(3,4),
                     (0,5),(1,5),(2,5),(3,5),
                     (5,10),(6,10),(7,10),(8,10),(3,9),(4,9),(5,9),(6,9),
                     (2,8),(3,8),(4,8),(1,7),(2,7),(3,7),(1,6),(2,6),(3,6)]

        d["sun"] = self.make_sun()

        d["stars"] = self.make_stars()
        
        
        return d

    def make_stars(self):
        stars = []
        for i in range(40):
            stars+=[(random.randint(0,19),random.randint(0,19))]
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
        print final
        return final
        
        

    def create_picture_dict(self): #multi-color pics...
        d = {}
        

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
