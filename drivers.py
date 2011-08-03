import Queue
from threading import Timer

class Processor(object):
  def __init__(self, input_queue):
    self.input_queue = input_queue
    self.listeners = []
  def again(self, t):
    next_run = Timer(t, self.do)
    next_run.start()
  def do(self):
    """
    The do method should:
        Consider input in the input queue
        call self.again(timeDelay)
        call self.done(data) 
        In that order
    """
    raise NotImplementedError("proc must be defined")
  def done(self, data):
    [l.handle(data) for l in self.listeners]
    #todo [rcoh] - there should be a better way to do this.

  
class Listener(object):
  def handle(self, data):
    raise NotImplementedError("handle must be defined")
