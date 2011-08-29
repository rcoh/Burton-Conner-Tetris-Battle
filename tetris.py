#!/usr/bin/env python
"""
Tetris Tk - A tetris clone written in Python using the Tkinter GUI library.

Controls:
    Left/a      Move left
    Right/d     Move right
    Up/w        Rotate / add player
    Down/s      Move down / start game
"""

from time import sleep, time
import random
import sys
from renderer import PygameRenderer
from renderer import LedRenderer
from tetris_shape import *
from ddrinput import DdrInput
from ddrinput import DIRECTIONS
import pygame

TIME_LIMIT = 4 * 60  #seconds
LINES_TO_ADVANCE = 8 #num lines needed to advance to next level
LEVEL_SPEEDS = [700,550,400,250,150,110]

MAXX = 10
MAXY = 18
(LEFT, RIGHT, UP, DOWN, DROP, DIE) = range(6) 

COLORS = ["orange", "red", "green", "blue", "purple", "yellow", "magenta"]
LEVEL_COLORS = ["red", "orange", "yellow", "green", "blue", "purple"]

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
                            dx,dy = (0,1)
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
        if x < 0 or x >= self.max_x or y < -3 or y >= self.max_y:
            return False
        elif self.landed.has_key( (x, y) ):
            return False
        else:
            return True


#represents a player. each player has a board, other player's board,
#current shape, score, etc
class Player():
    def __init__(self, player_id, gs, myBoard, otherBoard):
        print "initialize player"
        self.id = player_id
        self.board = myBoard
        self.other_board = otherBoard
        self.score = 0
        self.gs = gs
        self.shape = self.get_next_shape()
        
    def handle_move(self, direction):
        #if you can't move then you've hit something
        if self.shape:
            if direction==UP:
                self.shape.rotate(clockwise=False)
            else:
                if not self.shape.move( direction ):
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
                            self.gs.state = "ending" #you lost!
                            print "ENDING GAME.... PLAYER",self.id,"LOST"
                            if self.gs.num_players == 2:
                                self.gs.winner = (self.id + 1) % 2
                            else:
                                self.gs.winner = self.id
                                
                        # do we go up a level?
                        if (self.gs.level < len(LEVEL_SPEEDS)-1 and 
                            self.score / LINES_TO_ADVANCE >= self.gs.level+1 ):
                            print "level",self.gs.level
                            self.gs.level+=1
                            self.gs.delay = LEVEL_SPEEDS[self.gs.level]
                        
                        # Signal that the shape has 'landed'
                        return False
        return True
        
    def get_next_shape( self ):
        #Randomly select which tetrominoe will be used next.
        the_shape = self.gs.shapes[ random.randint(0,len(self.gs.shapes)-1) ]
        return the_shape.check_and_create(self.board)

#contains variables that are shared between the players:
#levels, delay time, etc
class GameState():
    def __init__(self):
        self.shapes = [square_shape, t_shape,l_shape, reverse_l_shape,
                      z_shape, s_shape,i_shape ]
        self.num_players = 0
        self.level = 0 #levels go 0-9
        self.delay = LEVEL_SPEEDS[0]
        self.state = "waiting" #states: waiting (between games), playing, ending
        self.winner = None #winning player id
       
        
#runs the overall game. initializes both player and any displays
class TetrisGame(object):

    #one-time initialization for gui etc
    def __init__(self):
        print "initialize tetris"
        self.gui = [PygameRenderer(), LedRenderer()]
        self.input = DdrInput()
        while True:
            self.init_game()

    #initializes each game
    def init_game(self):
        print "init next game"
        self.boards = [Board(MAXX,MAXY), Board(MAXX,MAXY)]
        self.players = [None,None]
        self.gameState = GameState()
        self.board_animation(0,"up_arrow")
        self.board_animation(1,"up_arrow")
        self.start_time = None
        self.update_gui()
        self.handle_input() #this calls all other functions, such as add_player, start_game
       
    def add_player(self,num): # 0=left, 1=right
        print "adding player",num
        if self.players[num]==None:
            self.boards[num].clear()
            p = Player(num, self.gameState, self.boards[num], self.boards[(num+1)%2])
            self.players[num] = p
            self.board_animation(num,"down_arrow")
            self.gameState.num_players+=1
            self.update_gui()
        
    def start_game(self):
        print "start game"
        self.boards[0].clear()
        self.boards[1].clear()
        self.gameState.state = "playing"
        self.update_gui()
        self.start_time = time()
        self.drop_time = time()
        self.gravity()

    def handle_input(self):
        
        game_on = True
        t = 0
        while game_on:
            t+=1
            
            if (self.gameState.state=="ending") or (self.gameState.state=="playing" and time()-self.start_time > TIME_LIMIT):
                print "GAME OVER"
                self.end_game()
                game_on = False
                return
            if self.gameState.state=="playing" and time()-self.drop_time > self.gameState.delay/1000.0:
                self.gravity()
                self.drop_time = time()
                if self.gameState.state != "ending":
                    self.update_gui()
                
            ev = self.input.poll()
            if ev:
                player,direction = ev
                #print "Player",player,direction
                if direction == DIE: #Exit instruction
                    game_on = False
                    pygame.quit()
                    sys.exit()
                if self.gameState.state=="playing":
                    if self.players[player]!=None:
                        #DROP is only for debugging purposes for now, to make the game end.
                        if direction == DROP:
                            while self.players[player].handle_move( DOWN ):
                                pass
                        else:
                            self.players[player].handle_move(direction)
                elif self.gameState.state == "waiting":
                    if direction==UP:
                        self.add_player(player)
                    elif direction==DOWN:
                        if self.players[player]!=None:
                            self.start_game()
                
                
         
            elif t%10000==0:
                t=0
                self.update_gui()
                
                
                
    def gravity(self):
        for p in self.players:
            if p:
                p.handle_move(DOWN)
            
    def update_gui(self):
        [gui.render_game(self.to_dict()) for gui in self.gui]

    def end_game(self):
        if self.gameState.winner!=None:
            winner_id = self.gameState.winner
            print "in end_game; player",winner_id,"wins"
        else:
            if self.gameState.num_players == 2:
                if self.players[0].score > self.players[1].score:
                    winner_id = 0
                elif self.players[1].score > self.players[0].score:
                    winner_id = 1
                else:
                    winner_id = 2 #tie, show both as winners.
            elif self.players[0]!=None:
                winner_id = 0
            else:
                winner_id = 1
        self.animate_ending(winner_id)

    def board_animation(self, board_id, design, color="green"):
        b = self.boards[board_id]
        d = self.create_shapes(design)
        for coord in d:
            b.landed[coord]=color
                        
    def animate_ending(self,winner_board):
        print "game over, display animation"
        if winner_board == 2:
            self.board_animation(0,"outline")
            self.board_animation(1,"outline")
        else:
            self.board_animation(winner_board,"outline","yellow")
        self.update_gui()
        sleep(3)

    def create_shapes(self,design): #in progress.....
        shapes = {}
        y = 4
        up_diags = [(1,y+4),(1,y+3),(2,y+3),(2,y+2),(3,y+2),(3,y+1),
                 (8,y+4),(8,y+3),(7,y+3),(7,y+2),(6,y+2),(6,y+1)]
        down_diags = [(x0,10-y0+2*y) for (x0,y0) in up_diags]
        line = [(i,j) for i in [4,5] for j in range(y,y+11)]
        up_arrow = line[:]
        for xy in up_diags:
            up_arrow.append(xy)
        down_arrow = line[:]
        for xy in down_diags:
            down_arrow.append(xy)
        sides = [(i,j) for i in [0,9] for j in range(18)]
        tb = [(i,j) for i in range(10) for j in [0,17]]
        outline = tb + sides
            
        shapes["down_arrow"] = down_arrow
        shapes["up_arrow"] = up_arrow
        shapes["outline"] = outline
        shapes["test"] = [(5,5)]
        
        return shapes[design]

    def to_dict(self):
        d = {}
        for n in range(2):
            board = self.boards[n]
            offset = n*MAXX
            
            #blocks
            for (x,y) in board.landed:
                d[(x+offset,y)] = board.landed[(x,y)]

            if self.players[n]!=None:
                p = self.players[n]

                #shapes
                if p.shape:
                    blocks = p.shape.blocks
                    for b in blocks:
                        if b.y >= 0:
                            d[(b.x+offset*n,b.y)] = b.color
            
                #score  
                score = p.score
                for i in range(10):
                    bit = score%2
                    score = score>>1
                    coord = (MAXX-1-i + offset, MAXY+1)
                    if bit:
                        d[coord] = "yellow"

                #level
                level = self.gameState.level
                d[(level+offset,MAXY)] = LEVEL_COLORS[level]

                #time
                if self.start_time!=None:
                    time_left = (self.start_time + TIME_LIMIT - time()) #seconds left
                    for i in range(TIME_LIMIT/60): #0,1,2,3 (minutes)
                        if time_left/60 >= i:
                            seconds = time_left - 60*i # is in .5-1 secs, etc
                            if not (.5<seconds<1.0 or 1.5<seconds<2.0 or 2.5<seconds<3.0):
                                coord = (MAXX-1-i + offset, MAXY)
                                d[coord] = "white"
                        
        return d
        
        
if __name__ == "__main__":
    tetrisGame = TetrisGame()
