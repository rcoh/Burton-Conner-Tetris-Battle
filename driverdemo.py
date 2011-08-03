from drivers import *
from threading import * 
import Queue
class TestProcessor(Processor):
  def do(self):
    data = []
    if not self.input_queue.empty():
      data.append(self.input_queue.get(False))
    self.again(.1)
    self.done(data)

class TestListener(Listener):
  def handle(self, data):
    print data
    print active_count()

def addToQueue():
  queue.put("test")
  again = Timer(.5, addToQueue)
  again.start()

queue = Queue.Queue()
t = TestProcessor(queue)
l = TestListener()
t.listeners.append(l)
queue = t.input_queue
t.do()
addToQueue()


