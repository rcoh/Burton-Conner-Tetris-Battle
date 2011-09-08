# renderer.py
# Copyright (C) 2011  Russell Cohen <rcoh@mit.edu>,
#                     Leah Alpert <lalpert@mit.edu>
#
# This file is part of Burton-Conner Tetris Battle.
#
# Burton-Conner Tetris Battle is free software: you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Burton-Conner Tetris Battle is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Burton-Conner Tetris Battle.  If not, see
# <http://www.gnu.org/licenses/>.

from numpy import zeros

import pygame
from pygame.locals import Color

import util

class Renderer(object):
  def render_game(self, game_board):
    """
    renderBoard
    @param game_board -- dictionary of tuples of location (x,y), 0 indexed from
    the top left of the board.
    """
    raise NotImplementedError

  def color_deref(self, color_str):
    return Color(color_str)
     
class PygameRenderer(Renderer):
 
  """
  Based heavily off of PygameRenderer in SmootLight.  Renders Tetris to a 
  pygame Window.
  """

  OFFSET = (50, 50)
  SCALE = 20
  RADIUS = 7
  DISPLAY_SIZE = (1500,1500)
  BETWEEN_BOARDS = 0 #scale units
  
  def __init__(self):
    pygame.init()
    self.screen = pygame.display.set_mode(self.DISPLAY_SIZE)
    self.background = pygame.Surface(self.screen.get_size())
    self.background = self.background.convert()
    self.background.fill(Color(0,0,0))

  def render_game(self, game_board):
    self.background.fill(Color(0,0,0))
    x0 = self.OFFSET[0] - self.SCALE/2 #- 3
    y0 = self.OFFSET[1] - 10
    x1 = self.OFFSET[0] + self.SCALE/2  + 9*self.SCALE #+ 3
    y1 = self.OFFSET[1] + 19.5*self.SCALE
    b2 = self.SCALE * 10 #x offset for second board
    line_endpoints = [((x0,y0), (x0,y1)), ((x0,y1), (x1,y1)), ((x1,y1), (x1,y0)), ((x1,y0), (x0,y0)),
                      ((x0,y1 - self.SCALE), (x1,y1 - self.SCALE)), ((x0,y1 - 2*self.SCALE), (x1,y1 - 2*self.SCALE))]
    for p1,p2 in line_endpoints:
      pygame.draw.line(self.background, self.color_deref("white"), p1, p2)
      pygame.draw.line(self.background, self.color_deref("white"), (p1[0]+b2,p1[1]),(p2[0]+b2,p2[1]))

    x_mid = (x0+x1)/2
    pygame.draw.line(self.background, self.color_deref("white"), (x_mid,y1 - self.SCALE),(x_mid,y1 - 2*self.SCALE))
    pygame.draw.line(self.background, self.color_deref("white"), (x_mid+b2,y1 - self.SCALE),(x_mid+b2,y1 - 2*self.SCALE))

    for (x,y) in game_board:
      if x >= 0 and x < 20 and y >= 0 and y < 20:
        disp_x = x
        pygame.draw.circle(self.background, self.color_deref(game_board[(x,y)]), 
            (self.OFFSET[0] + disp_x*self.SCALE, self.OFFSET[1] + y*self.SCALE), self.RADIUS)
      
    self.screen.blit(self.background, (0,0))
    pygame.display.flip()

class LedRenderer(Renderer):
  """
  Renderer for the LEDs.  Based heavily on IndoorRenderer in Smootlight and 
  general Smootlight abstraction patterns
  """
  POWER_SUPPLY_IPS = ['10.32.0.32','10.32.0.32', '10.32.0.31',
                      '10.32.0.31','10.32.0.35','10.32.0.35','10.32.0.33','10.32.0.33'] #TODO: Fill in
  SOCK_PORT = 6038
  sockets = {}
 
  def render_game(self, game_board):
    packets = self.map_to_packets(game_board)
    
    packets_with_destinations = zip(self.POWER_SUPPLY_IPS, packets)
    for (ip, (port, packet)) in packets_with_destinations:
      if not ip in self.sockets:
        self.sockets[ip] = util.getConnectedSocket(ip, self.SOCK_PORT)
      final_packet = util.composePixelStripPacket(packet, port) 
      try:
        if self.sockets[ip] != None:
          self.sockets[ip].send(final_packet, 0x00)
      except:
        print 'failure sending packet'
  def color_deref(self, color):
    return Color(color)[0:3]
  def fake_map_to_packets(self, game_board):
    strip = zeros((50,3), 'ubyte')
    strip[:] = (255,255,0)
    return [(1, strip), (2, strip)] * 4
  def map_to_packets(self, game_board):
    """
    Performs the mapping between a game_board and a list of (port,packet) pairs.  The port,packet
    pairs should line up with the ip's in IP_ADDRESSES
    """
    #This is hardcoded, mostly because I'm curious of the complexity
    packets = []
    board_x_min = 0
    board_x_max = 9 
    section_width = 10
    section_height = 5
    board_x_min = 0
    #left board
    for board_y_min in [14, 9, 4, -1]:
      strip = zeros((50,3),'ubyte')
      index = 0
      for y in range(board_y_min+section_height, board_y_min, -1): #for each strip
        strand_dir = -1 if y % 5 % 2 == 0 else 1 #direction alternates within strip
        left_x = board_x_min+section_width-1 if strand_dir < 0 else board_x_min
        right_x = board_x_min-1 if strand_dir < 0 else board_x_min+section_width
        for x in range(left_x, right_x, strand_dir):
          #strip[index] = (x*10,0,y*10)
          if (x,y) in game_board:
            strip[index] = self.color_deref(game_board[(x,y)]) 
          index += 1
      packets.append((1+(len(packets) % 2), strip)) #port alternates by strip
    #right board:
    board_x_min = 10
    for board_y_min in [15, 10, 5, 0]:
      strip = zeros((50,3),'ubyte')
      index = 0
      for y in range(board_y_min, board_y_min + section_height ): #for each strip
        strand_dir = 1 if y % 5 % 2 == 0 else -1 #direction alternates within strip
        left_x = board_x_min+section_width-1 if strand_dir < 0 else board_x_min
        right_x = board_x_min-1 if strand_dir < 0 else board_x_min+section_width
        for x in range(left_x, right_x, strand_dir):
          #strip[index] = (x*10,0,y*10)
          if (x,y) in game_board:
            strip[index] = self.color_deref(game_board[(x,y)]) 
          index += 1
      packets.append((1+(len(packets) % 2), strip)) #port alternates by strip
    return packets
