"""
This is the class you run to run tetris.
Handles input and output
"""

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
        #height = rows + one blank + score row
        #width = left board + 4 blank + right board
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
    """
    def draw_board(self, color_dict):
        self.canvas.delete(ALL)
        #ARRAY or DICT...
        for b in color_dict:
            self.add_block(b)
    """           
    def draw_board(self, players):
        self.canvas.delete(ALL)
        x_width = self.max_x*self.scale+3
        y_width = self.max_y*self.scale+3
        gap = 4*self.scale
        self.canvas.create_rectangle(3,2,x_width, y_width)
        self.canvas.create_rectangle(x_width+gap,2,2*x_width+gap-3, y_width)
        offset = 0
        for p in players:
            landed = p.board.landed
            for b in landed:
                self.add_block((b[0]+offset, b[1]), landed[b])
            for b in p.shape.blocks:
                self.add_block((b.x+offset, b.y), b.color)
            offset += (self.max_x + 4)
       
        self.display_score(players[0].score,0)
        self.display_score(players[1].score,1)

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
              
"""   
def update_display(player1,player2)
    nah = process(meh)
    #debug mode:
    display_image(nah)
    #real mode:
    #update_lights(nah)
    

#waiting
#press
start = false
while (!start)
if (get_press(p0s)and p0_is_in) or (p1s and p1_is_in):
    start = true
if get_press(p0in):
    game.add_player(0)
if p1in:
    game.add_player(1)

animate countdown

#assume 1p
handle controls...
p0.left()
p0.right()
etc

get state...
if p0.update()...
    update_display(p0.board, p0.score)
    
if p0.died:
    end

animate end_seq(score)

goto waiting


"""
