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

class PygameGoodRenderer(Renderer):
 
  """
  Based heavily off of PygameRenderer in SmootLight.  Renders Tetris to a 
  pygame Window.
  """

  DISPLAY_SIZE = (1000,1000)
  OFFSET = (50, 50)
  SCALE = 20 
  RADIUS = 6
  
  def __init__(self):
    pygame.init()
    self.screen = pygame.display.set_mode(self.DISPLAY_SIZE)
    self.background = pygame.Surface(self.screen.get_size())
    self.background = self.background.convert()
    self.background.fill(Color(0,0,0))

  def render_game(self, game_board):
    self.background.fill(Color(0,0,0))
    x0 = self.OFFSET[0] - 1
    y0 = self.OFFSET[1] - 1
    x1 = self.OFFSET[0] + 10*self.SCALE
    y1 = self.OFFSET[1] + 20*self.SCALE - 1
    b2 = self.SCALE * 13 #x offset for second board
    line_endpoints = [((x0,y0), (x0,y1)), ((x0,y1), (x1,y1)), ((x1,y1), (x1,y0)), ((x1,y0), (x0,y0)),
                      ((x0,y1 - 15), (x1,y1 - 15)), ((x0,y1 - 30), (x1,y1 - 30))]
    for p1,p2 in line_endpoints:
      pygame.draw.line(self.background, self.color_deref("white"), p1, p2)
      pygame.draw.line(self.background, self.color_deref("white"), (p1[0]+b2,p1[1]),(p2[0]+b2,p2[1]))

    x_mid = (x0+x1)/2 + self.SCALE
    pygame.draw.line(self.background, self.color_deref("white"), (x_mid,y1 - 15),(x_mid,y1 - 30))
    pygame.draw.line(self.background, self.color_deref("white"), (x_mid+b2,y1 - 15),(x_mid+b2,y1 - 30))

    for (x,y) in game_board:
      disp_x = x
      if x >= 10:
        disp_x+=3
      pygame.draw.rect(self.background, self.color_deref(game_board[(x,y)]), 
          (self.OFFSET[0] + disp_x*self.SCALE, self.OFFSET[1] + y*self.SCALE, self.SCALE-1, self.SCALE-1))
      
    self.screen.blit(self.background, (0,0))
    pygame.display.flip()
     
class PygameRenderer(Renderer):
 
  """
  Based heavily off of PygameRenderer in SmootLight.  Renders Tetris to a 
  pygame Window.
  """

  DISPLAY_SIZE = (1500,1500)
  OFFSET = (50, 50)
  SCALE = 20 
  RADIUS = 6
  
  def __init__(self):
    pygame.init()
    self.screen = pygame.display.set_mode(self.DISPLAY_SIZE)
    self.background = pygame.Surface(self.screen.get_size())
    self.background = self.background.convert()
    self.background.fill(Color(0,0,0))

  def render_game(self, game_board):
    self.background.fill(Color(0,0,0))
    x0 = self.OFFSET[0] - self.SCALE/2 - 3
    y0 = self.OFFSET[1] - 10
    x1 = self.OFFSET[0]+8 + 9*self.SCALE
    y1 = self.OFFSET[1]+8 + 19*self.SCALE
    b2 = self.SCALE * 13 #x offset for second board
    line_endpoints = [((x0,y0), (x0,y1)), ((x0,y1), (x1,y1)), ((x1,y1), (x1,y0)), ((x1,y0), (x0,y0)),
                      ((x0,y1 - 16), (x1,y1 - 16)), ((x0,y1 - 31), (x1,y1 - 31))]
    for p1,p2 in line_endpoints:
      pygame.draw.line(self.background, self.color_deref("white"), p1, p2)
      pygame.draw.line(self.background, self.color_deref("white"), (p1[0]+b2,p1[1]),(p2[0]+b2,p2[1]))

    x_mid = (x0+x1)/2 + self.SCALE
    pygame.draw.line(self.background, self.color_deref("white"), (x_mid,y1 - 16),(x_mid,y1 - 31))
    pygame.draw.line(self.background, self.color_deref("white"), (x_mid+b2,y1 - 16),(x_mid+b2,y1 - 31))

    for (x,y) in game_board:
      disp_x = x
      if x >= 10:
        disp_x+=3
      pygame.draw.circle(self.background, self.color_deref(game_board[(x,y)]), 
          (self.OFFSET[0] + disp_x*self.SCALE, self.OFFSET[1] + y*self.SCALE), self.RADIUS)
      
    self.screen.blit(self.background, (0,0))
    pygame.display.flip()

class LedRenderer(Renderer):
  """
  Renderer for the LEDs.  Based heavily on IndoorRenderer in Smootlight and 
  general Smootlight abstraction patterns
  """
  POWER_SUPPLY_IPS = ['10.32.97.17',0,0,0] #TODO: Fill in
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
    return (255, 0, 0)
  def map_to_packets(self, game_board):
    """
    Performs the mapping between a game_board and a list of (port,packet) pairs.  The port,packet
    pairs should line up with the ip's in IP_ADDRESSES
    """
    #This is hardcoded, mostly because I'm curious of the complexity
    packets = []
    board_x_min = 0
    board_x_max = 10
    section_width = 10
    section_height = 5
    for board_x_min in [0, 10]:
      packet = []
      for board_y_min in [20, 15, 10, 5]:
        strip = zeros((50,3),'ubyte')
        index = 0
        for y in range(board_y_min, board_y_min-section_height, -1): 
          for x in range(board_x_min+section_width, board_x_min, -1):
            if (x,y) in game_board:
              strip[index] = self.color_deref(game_board[(x,y)]) 
        packet.append((1+len(packet), strip))
        index += 1
      packets += packet
    return packets
