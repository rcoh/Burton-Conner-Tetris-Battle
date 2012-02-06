#!/usr/bin/env python
# Burton-Conner Tetris Battle -- Tetris installation controlled by DDR pads
# Copyright (C) 2010, 2011  Simon Peverett <http://code.google.com/u/@WRVXSlVXBxNGWwl1/>
# Copyright (C) 2011  Russell Cohen <rcoh@mit.edu>,
#                     Leah Alpert <lalpert@mit.edu>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
TRON

Controls:
    Left/a      Move left
    Right/d     Move right
    Up/w        Move up / add player
    Down/s      Move down / start game
"""

from time import sleep, time
import random
import sys
from renderer import PygameGoodRenderer
from renderer import PygameRenderer
from renderer import LedRenderer
from ddrinput import DdrInput
from ddrinput import DIRECTIONS
import pygame

TIME_LIMIT = 5 * 60  #seconds
LINES_TO_ADVANCE = 8 #num lines needed to advance to next level
LEVEL_SPEEDS = [200,150]

MAXX = 20
MAXY = 18
(LEFT, RIGHT, UP, DOWN, DROP, DIE) = range(6) 
MOVES = {LEFT:(-1,0), RIGHT:(1,0), UP:(0,-1), DOWN:(0,1)}

LEVEL_COLORS = ["red", "orange", "yellow", "green", "blue", "purple"]

#represents a player. each player has a board, current direction, score, etc
class Player():
    def __init__(self, player_id, gs, board):
        self.id = player_id
        self.board = board
        x_pos = [3, MAXX - 4][player_id]
        print "player id= ", player_id
        print "x_pos = ", x_pos
        self.position = (x_pos, MAXY/2)
        self.score = 0
        self.gs = gs
        self.direction = [RIGHT,LEFT][player_id] #0 is right, 1 is left

    def handle_move(self, d):
        #add handling for case when dir is opposite direction of movement
        if (self.direction==LEFT and d==RIGHT) or (self.direction==RIGHT and d==LEFT) or (self.direction==UP and d==DOWN) or (self.direction==DOWN and d==UP): 
            return
        else:
            self.direction = d

    def move_tron(self):
        old_pos = self.position
        self.position = (self.position[0] + MOVES[self.direction][0],
                         self.position[1] + MOVES[self.direction][1])
        if self.position in self.board or self.position[0] < 0 or self.position[0] >= MAXX or self.position[1] < 0 or self.position[1] >= MAXY:
            #you hit something, you lose!
            self.gs.state = "ending"
            self.gs.winner = [self.id, (self.id + 1) % 2][self.gs.num_players - 1]
            self.board[old_pos] = 2 #yellow
            return
        else:
            self.board[self.position] = self.id

#contains variables that are shared between the players:
#levels, delay time, etc
class GameState():
    def __init__(self):
        self.num_players = 0
        self.level = 0 #levels go 0-9
        self.delay = LEVEL_SPEEDS[0]
        self.state = "waiting" #states: waiting (between games), playing, ending
        self.winner = None #winning player id

#runs the overall game. initializes both player and any displays
class TronGame(object):

    #one-time initialization for gui etc
    def __init__(self):
        print "initialize tetris"
        self.gui = [PygameGoodRenderer(), LedRenderer()]
        self.input = DdrInput()
        while True:
            self.init_game()

    #initializes each game
    def init_game(self):
        print "init next game"
        self.animation = {}
        self.board = {}
        self.players = [None,None]
        self.gameState = GameState()
        self.board_animation(0,"up_arrow")
        self.board_animation(1,"up_arrow")
        self.start_time = None
        self.input.reset()
        self.update_gui()
        self.handle_input() #this calls all other functions, such as add_player, start_game

    def add_player(self,num): # 0=left, 1=right
        print "adding player",num
        if self.players[num]==None:
            p = Player(num, self.gameState, self.board)
            self.players[num] = p
            self.board_animation(num,"down_arrow")
            self.gameState.num_players+=1
            self.update_gui()

    def start_game(self):
        print "start game"
        self.animation.clear()
        self.gameState.state = "playing"
        self.start_time = time()
        self.drop_time = time()
        self.gravity()

    def handle_input(self):
        game_on = True
        t = 0
        while game_on:
            t+=1

            if (self.gameState.state=="ending") or (self.gameState.state=="playing" and time()-self.start_time > TIME_LIMIT):
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
                if self.gameState.state=="playing" and self.players[player]!=None:
                    self.players[player].handle_move(direction)
                elif self.gameState.state == "waiting":
                    if direction==UP:
                        self.add_player(player)
                    elif direction==DOWN:
                        if self.players[player]!=None:
                            self.start_game()

                self.update_gui()

            elif t%10000==0:
                t=0
                self.update_gui()

    #this makes the players move            
    def gravity(self):
        for p in self.players:
            if p:
                p.move_tron()

    def update_gui(self):
        d = self.to_dict()
        [gui.render_game(d) for gui in self.gui]
        #self.gui[0].render_game(self.to_gui_dict())

    def end_game(self):
        if self.gameState.winner!=None:
            winner_id = self.gameState.winner
            print "GAME OVER: player",winner_id,"wins"
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

    def board_animation(self, board_id, design, color=1):
        d = self.create_shapes(design)
        for coord in d:
            c = (coord[0] + board_id * MAXX/2, coord[1])
            self.animation[c]=color

    def animate_ending(self,winner_board):
        if winner_board == 2:
            self.board_animation(0,"outline")
            self.board_animation(1,"outline")
        else:
            self.board_animation(winner_board,"outline",2)
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
        shapes["whole_outline"] = outline
        shapes["test"] = [(5,5)]

        return shapes[design]

    def to_dict(self):
        player_colors = ["red", "green", "yellow"]
        d = {}

        for (x,y) in self.board:
            d[(x,y)] = player_colors[self.board[(x,y)]]

        for (x,y) in self.animation:
            d[(x,y)] = player_colors[self.animation[(x,y)]]

        for n in range(2):
            if self.players[n]!=None:
                p = self.players[n]
                offset = n*(MAXX/2)

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
                                coord = (MAXX/2-1-i + offset, MAXY)
                                d[coord] = "white"

        return d
    """
    def to_gui_dict(self):
        d = {}
        if self.start_time!=None:
            d[(2,'level')] = self.gameState.level
            d[(2,'time_left')] = self.start_time + TIME_LIMIT - time()

        for n in range(2):
            board = self.boards[n]
            offset = n*MAXX

            #blocks
            for (x,y) in board.landed:
                d[(x+offset,y)] = board.landed[(x,y)]

            if self.players[n]!=None:
                p = self.players[n]
                #score
                d[(n,"score")] = p.score

                #shapes
                if p.shape:
                    blocks = p.shape.blocks
                    for b in blocks:
                        if b.y >= 0:
                            d[(b.x+offset*n,b.y)] = b.color

        return d
      """    

if __name__ == "__main__":
    print """Burton-Conner Tetris Battle  Copyright (C) 2010, 2011  Simon Peverett
                             Copyright (C) 2011 Russell Cohen, Leah Alpert
This program comes with ABSOLUTELY NO WARRANTY; for details see
<http://gnu.org/licenses/gpl#section15>.
This is free software, and you are welcome to redistribute it under certain
conditions; see <http://gnu.org/licenses/gpl#content> for details."""

    tronGame = TronGame()
