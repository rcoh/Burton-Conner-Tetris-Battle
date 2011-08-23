#!/usr/bin/env python
"""
Tetris Tk - A tetris clone written in Python using the Tkinter GUI library.

Controls:
    Left/a      Move left
    Right/d     Move right
    Up/w        Rotate / add player
    Down/s      Move down / start game
"""
from Tkinter import *
from time import sleep
import random
import sys
from tetrisGUI import GUI
from tetris_shape import *

MAXX = 10
MAXY = 18
NO_OF_LEVELS = 10

LEFT = "left"
RIGHT = "right"
DOWN = "down"
direction_d = { "left": (-1, 0), "right": (1, 0), "down": (0, 1) }

COLORS = ["orange", "red", "green", "blue", "purple", "yellow", "magenta"]
#COLORS = ["gray"]

class Board():
    """
    The board represents the tetris playing area. A grid of x by y blocks.
    Stores blocks that have landed.
    """
    def __init__(self, max_x=10, max_y=20): 
        # blocks are stored in dict of (x,y)->"color"
        self.landed = {}
        self.max_x = max_x
        self.max_y = max_y

    def clear(self):
        self.landed = {}
      
    def receive_lines(self, num_lines):
        #shift lines up
        for y in range(self.max_y-num_lines):
            for x in xrange(self.max_x):
                block_color = self.landed.pop((x,y+num_lines),None)
                if block_color:
                    self.landed[(x,y)] = block_color
        #put in new lines
        for j in range(num_lines):
            for i in random.sample(xrange(self.max_x), random.choice([6,7])):
                self.landed[(i,self.max_y-1-j)] = random.choice(COLORS)
                
    def check_for_complete_row( self, blocks ):
        """
        Look for a complete row of blocks, from the bottom up until the top row
        or until an empty row is reached.
        """
        rows_deleted = 0
        
        # Add the blocks to those in the grid that have already 'landed'
        for block in blocks:
            self.landed[ block.coord() ] = block.color
        
        empty_row = 0
        # find the first empty row
        for y in xrange(self.max_y -1, -1, -1):
            row_is_empty = True
            for x in xrange(self.max_x):
                if self.landed.get((x,y), None):
                    row_is_empty = False
                    break;
            if row_is_empty:
                empty_row = y
                break

        # Now scan up and until a complete row is found. 
        y = self.max_y - 1
        while y > empty_row:
 
            complete_row = True
            for x in xrange(self.max_x):
                if self.landed.get((x,y), None) is None:
                    complete_row = False
                    break;

            if complete_row:
                rows_deleted += 1
                
                #delete the completed row
                for x in xrange(self.max_x):
                    self.landed.pop((x,y))
                    
                # move all the rows above it down
                for ay in xrange(y-1, empty_row, -1):
                    for x in xrange(self.max_x):
                        block_color = self.landed.pop((x,ay), None)
                        if block_color:
                            dx,dy = direction_d[DOWN]
                            self.landed[(x+dx, ay+dy)] = block_color

                # move the empty row index down too
                empty_row +=1
                # y stays same as row above has moved down.       
            else:
                y -= 1
            
        # return the number of rows deleted.        
        return rows_deleted

    def check_block( self, (x, y) ):
        """
        Check if the x, y coordinate can have a block placed there.
        That is; if there is a 'landed' block there or it is outside the
        board boundary, then return False, otherwise return true.
        """
        if x < 0 or x >= self.max_x or y < 0 or y >= self.max_y:
            return False
        elif self.landed.has_key( (x, y) ):
            return False
        else:
            return True

#represents a player. each player has a board and can get new shapes...
#
class Player():
    def __init__(self, gs, myBoard, otherBoard):
        print "initialize player"
        self.board = myBoard
        self.other_board = otherBoard
        self.score = 0
        self.gs = gs
        self.shape = self.get_next_shape()
        
    def handle_move(self, direction):
        #if you can't move then you've hit something
        success = self.shape.move( direction )
        if not success:
                
            # if you're heading down then the shape has 'landed'
            if direction == DOWN:
                points = self.board.check_for_complete_row(
                    self.shape.blocks)
                #del self.shape
                self.shape = self.get_next_shape()
                
                self.score += points
                if self.gs.num_players == 2:
                    if points > 1:
                        self.other_board.receive_lines(points-1) 
   
                # If the shape returned is None, then this indicates that
                # that the check before creating it failed and the
                # game is over!
                if self.shape is None:
                    self.gs.state = "ending" #loss!
                    self.gs.winner = self.other_board
                    #self.status = "loss"
                
                # do we go up a level?
                if (self.gs.level < NO_OF_LEVELS and 
                    self.score >= self.gs.thresholds[self.gs.level]):
                    self.gs.level+=1
                    self.gs.delay-=100
                
                # Signal that the shape has 'landed'
                return False
        return True

    def left(self):
        if self.shape:
            self.handle_move( LEFT )
        
    def right(self):
        if self.shape:
            self.handle_move( RIGHT )
            
    def down(self):
        if self.shape:
            self.handle_move( DOWN )
            
    def up(self):
        if self.shape:
            self.shape.rotate(clockwise=False)
 
    def move_my_shape( self ):
        if self.shape:
            self.handle_move( DOWN )
        
    def get_next_shape( self ):
        #Randomly select which tetrominoe will be used next.
        the_shape = self.gs.shapes[ random.randint(0,len(self.gs.shapes)-1) ]
        return the_shape.check_and_create(self.board)

#contains variables that are shared between the players:
#levels, delay time, etc?
class GameState():
    def __init__(self, gui):
        self.shapes = [square_shape, t_shape,l_shape, reverse_l_shape,
                      z_shape, s_shape,i_shape ]
        self.num_players = 0
        self.level = 1
        self.delay = 800
        self.thresholds = range(10,100,10)
        self.state = "waiting" #states: waiting, playing, ending
        self.winner = None #winning Board
       
        
#runs the overall game. initializes both player and any displays
class TwoPlayerGame(object):

    #one-time initialization for gui etc
    def __init__(self, parent):
        print "initialize tetris"
        self.parent = parent
        self.gui = GUI(parent,20,MAXX,MAXY)
        self.gui.pack(side=BOTTOM)
        self.parent.bind("<Key>", self.handle_key_press)
        self.init_game()

    #initializes each game
    def init_game(self):
        print "init next game"
        board0 = Board(MAXX,MAXY)
        board1 = Board(MAXX,MAXY)
        self.boards = [board0, board1]
        self.gameState = GameState(self.gui)
        self.players = [None,None]
        self.update_gui()
        self.gameState.state = "waiting" #states are waiting, playing, ending

    def add_player(self,num): # 0=left, 1=right
        if self.players[num]==None:
            p = Player(self.gameState, self.boards[num], self.boards[(num+1)%2])
            self.players[num] = p
            self.update_gui()
            self.gameState.num_players+=1
        
    def start_game(self):
        print "start game"
        self.gameState.state = "playing"
        self.parent.after( self.gameState.delay, self.gravity)
        self.update_gui()

    #handles gravity and checks for game over
    def gravity(self): #probably shouldn't handle gravity and endgame...or rename?
        if self.gameState.state == "ending":
            self.end_game()
            return
        else:
            for p in self.players:
                if p:
                    p.move_my_shape()
            self.update_gui()
            self.parent.after( self.gameState.delay, self.gravity)

    def handle_key_press(self,event):
        k = event.keysym
        if self.gameState.state == "playing":
            if self.players[1]:
                if k=="Left":
                    self.players[1].left()
                elif k=="Right":
                    self.players[1].right()
                elif k=="Down":
                    self.players[1].down()
                elif k=="Up":
                    self.players[1].up()
            if self.players[0]:
                if k=="a":
                    self.players[0].left()
                elif k=="d":
                    self.players[0].right()
                elif k=="s":
                    self.players[0].down()
                elif k=="w":
                    self.players[0].up()
        elif self.gameState.state == "waiting":
            if k=="Up":
                self.add_player(1)
            elif k=="w":
                self.add_player(0)
            elif k=="Down" and self.players[1]!=None:
                self.start_game()
            elif k=="s" and self.players[0]!=None:
                self.start_game()
        #if state==ending, ignore input
        self.update_gui()
            
    def update_gui(self):
        self.gui.draw_board(self.players)

    def end_game(self):
        winner_board = self.gameState.winner
        self.animate_ending(winner_board)
        self.init_game()

    def animate_ending(self,winner_board):
        print "game over, display animation"
        for i in range(100):
            print i,
        
    def end_all(self):
        #this will destory the gui. not really useful.
        Toplevel().destroy()
        self.parent.destroy()
        sys.exit(0)

    def to_dict(self):
        d = {}
        for n in range(2):
            #in progress...
            p = players[n]
            offset = n*self.max_x
            
            #blocks
            for (x,y) in p.board.landed:
                d[(x+offset,y)] = p.board.landed[xy]
                
            #shapes
            blocks = p.shape.blocks
            for b in blocks:
                d[(b.x+offset*n,b.y)] = b.color
        
            #score
            for i in range(10):
                score = p.score
                bit = score%2
                score = score>>1
                coord = (self.max_x-1-i + offset, self.max_y+1)
                if bit:
                    d[coord] = "yellow"
                else:
                    d[coord] = "gray"
        
        
if __name__ == "__main__":
    root = Tk()
    root.title("Tetris Tk")
    theGame = TwoPlayerGame( root )
    root.mainloop()
