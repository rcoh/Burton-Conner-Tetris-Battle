from ddrinput import DdrInput
from ddrinput import DIRECTIONS
from ddrinput import LEFT,RIGHT,UP,DOWN
d = DdrInput()
while 1:
  ev = d.poll()
  if ev:
    player,direction = ev
    print 'Player', int(player), DIRECTIONS[direction] 
