"""
This is the class you run to run tetris.
Handles input and output
"""

#make this more display-independent, yo.


from Tkinter import *

#GUI
class GUI( Frame ):
    def __init__(self, parent, scale=20, max_x=10, max_y=20, offset=3):
        print "initialize gui"
        """
       Init and config the tetris computer display
        """
        Frame.__init__(self, parent) 
        self.parent = parent
        self.scale = scale
        self.max_x = max_x
        self.max_y = max_y
        self.offset = offset
        self.canvas = Canvas(parent,
                             height=((max_y+2) * scale)+offset,
                             width= 2*((max_x+2) * scale)+offset)
        #size of one board plus buffer
        self.boardsize = ((max_x+4) * scale)+offset
        self.canvas.pack()
        
    def add_block(self, (x, y), color):
        """
        Draw a block on the canvas
        """
        shrink = 4
        rx = (x * self.scale) + self.offset
        ry = (y * self.scale) + self.offset 
        #self.canvas.create_oval(rx+shrink, ry+shrink, rx+self.scale-shrink,
        #ry+self.scale-shrink, width=0, fill=color)
        self.canvas.create_rectangle(
            rx, ry, rx+self.scale, ry+self.scale, fill=color
        )

    def display_dict(self,d):
        self.canvas.delete(ALL)
        x_width = self.max_x*self.scale+3
        y_width = self.max_y*self.scale+3
        gap = 4*self.scale
        self.canvas.create_rectangle(3,2,x_width, y_width)
        self.canvas.create_rectangle(x_width+gap,2,2*x_width+gap-3, y_width)
        for (x,y) in d:
            color = d[(x,y)]
            if x>self.max_x:
                x+=4
            self.add_block((x,y),color)
        
    def draw_board(self, players):
        self.canvas.delete(ALL)
        x_width = self.max_x*self.scale+3
        y_width = self.max_y*self.scale+3
        gap = 4*self.scale
        self.canvas.create_rectangle(3,2,x_width, y_width)
        self.canvas.create_rectangle(x_width+gap,2,2*x_width+gap-3, y_width)
        offset = 0
        for n in range(2):
            p = players[n]
            if p:
                offset = n*(self.max_x + 4)
                landed = p.board.landed
                for b in landed:
                    self.add_block((b[0]+offset, b[1]), landed[b])
                if p.shape:
                    for b in p.shape.blocks:
                        self.add_block((b.x+offset, b.y), b.color)
                self.display_score(p.score,n)

    def display_score(self, score, player_num):
        offset = player_num * (self.max_x + 4)
        for i in range(10):
            bit = score%2
            score = score>>1
            coord = (self.max_x-1-i + offset, self.max_y+1)
            if bit:
                self.add_block(coord, "yellow")
            else:
                self.add_block(coord, "gray")
