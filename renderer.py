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

import pygame
from pygame.locals import Color
class PygameRenderer(Renderer):
 
  """
  Based heavily off of PygameRenderer in SmootLight.  Renders Tetris to a 
  pygame Window.
  """

  DISPLAY_SIZE = (1000,1000)
  OFFSET = (100, 100)
  SCALE = 10
  
  def __init__(self):
    pygame.init()
    self.screen = pygame.display.set_mode(self.DISPLAY_SIZE)
    self.background = pygame.Surface(self.screen.get_size())
    self.background = self.background.convert()
    self.background.fill(Color(0,0,0))

  def render_game(self, game_board):
    self.background.fill(Color(0,0,0))
    for (x,y) in game_board:
      pygame.draw.circle(self.background, self.color_deref(game_board[(x,y)]), 
          (self.OFFSET[0] + x*self.SCALE, self.OFFSET[1] + y*self.SCALE), self.SCALE)
    self.screen.blit(self.background, (0,0))
    pygame.display.flip()

import util
class LedRenderer(Renderer):
  """
  Renderer for the LEDs.  Based heavily on IndoorRenderer in Smootlight and 
  general Smootlight abstraction patterns
  """
  POWER_SUPPLY_IPS = [0,0,0,0] #TODO: Fill in
  SOCK_PORT = 6038
  sockets = {}
 
  def render_game(self, game_board):
    packets = self.map_to_packets(game_board)
    packets_with_destinations = zip(self.POWER_SUPPLY_IPS, packets)
    for (ip, (port, packet)) in packets:
      if not ip in self.sockets:
        self.sockets[ip] = util.getConnectedSocket(ip, self.SOCK_PORT)
      final_packet = util.composePixelStripPacket(packet, port) 
      try:
        self.sockets[ip].send(packet, 0x00)
      except:
        print 'failure sending packet'
  
  def map_to_packets(game_board):
    """
    Performs the mapping between a game_board and a list of (port,packet) pairs.  The port,packet
    pairs should line up with the ip's in IP_ADDRESSES
    """
    #TODO(rcoh): Write this when we decide on a layout
