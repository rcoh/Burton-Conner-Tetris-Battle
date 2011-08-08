##############THIS IS THE ORIGINAL TETRIS CODE.##############
####PROVIDED ONLY FOR REFERENCE.  DON'T WORRY ABOUT IT.######                                                                
                                                                     
                                                                     
                                             
from graphics import *
import random

############################################################
# BLOCK CLASS
############################################################

class Block(Rectangle):
    ''' Block class:
        Implement a block for a tetris piece
        Attributes: x - type: int
                    y - type: int
        specify the position on the tetris board
        in terms of the square grid
    '''
    # BLOCK SIZE defined in pixels. So from now on, each coordinate is multiplied by 30
    # (see below)
    BLOCK_SIZE = 30
    OUTLINE_WIDTH = 3

    def __init__(self, pos, color):
        self.x = pos.x
        self.y = pos.y
        
        p1 = Point(pos.x*Block.BLOCK_SIZE + Block.OUTLINE_WIDTH,
                   pos.y*Block.BLOCK_SIZE + Block.OUTLINE_WIDTH)
        p2 = Point(p1.x + Block.BLOCK_SIZE, p1.y + Block.BLOCK_SIZE)

        Rectangle.__init__(self, p1, p2)
        self.setWidth(Block.OUTLINE_WIDTH)
        self.setFill(color)
        self.color = color

    def can_move(self, board, dx, dy):
        ''' Parameters: dx - type: int
                        dy - type: int

            Return value: type: bool
                        
            checks if the block can move dx squares in the x direction
            and dy squares in the y direction
            Returns True if it can, and False otherwise
            HINT: use the can_move method on the Board object
        '''

        if board.can_move(self.x + dx, self.y + dy) == True:
            return True
        return False
    
    def move(self, dx, dy):
        ''' Parameters: dx - type: int
                        dy - type: int
                        
            moves the block dx squares in the x direction
            and dy squares in the y direction
        '''

        self.x += dx
        self.y += dy

        Rectangle.move(self, dx*Block.BLOCK_SIZE, dy*Block.BLOCK_SIZE)


############################################################
# SHAPE CLASS
############################################################

class Shape():
    ''' Shape class:
        Base class for all the tetris shapes
        Attributes: blocks - type: list - the list of blocks making up the shape
                    rotation_dir - type: int - the current rotation direction of the shape
                    shift_rotation_dir - type: Boolean - whether or not the shape rotates
    '''

    def __init__(self, coords, color):
        # Define empty list
        self.blocks = []
        self.rotation_dir = 1
        ### A boolean to indicate if a shape shifts rotation direction or not.
        ### Defaults to false since only 3 shapes shift rotation directions (I, S and Z)
        self.shift_rotation_dir = False

        # for each coordinate, make a block object out of it and append to list
        for pos in coords:
            self.blocks.append(Block(pos, color))



    def get_blocks(self):
        '''returns the list of blocks
        '''
        #return list of blocks
        return self.blocks
        pass

    def draw(self, win):
        ''' Parameter: win - type: CanvasFrame

            Draws the shape:
            i.e. draws each block
        '''
        # For each block in list, draw block
        for block in self.blocks:
            block.draw(win)

    def move(self, dx, dy):
        ''' Parameters: dx - type: int
                        dy - type: int

            moves the shape dx squares in the x direction
            and dy squares in the y direction, i.e.
            moves each of the blocks
        '''
        for block in self.blocks:
            block.move(dx, dy)

    def can_move(self, board, dx, dy):
        ''' Parameters: dx - type: int
                        dy - type: int

            Return value: type: bool
                        
            checks if the shape can move dx squares in the x direction
            and dy squares in the y direction, i.e.
            check if each of the blocks can move
            Returns True if all of them can, and False otherwise
           
        '''
        
        #Checks each block to see if it can move dx and dy
        for blocks in self.blocks:
            if blocks.can_move(board, dx, dy) == False:
                return False
        return True
        # default implementation (MUST CHANGE)
        #return True
    
    def get_rotation_dir(self):
        ''' Return value: type: int
        
            returns the current rotation direction
        '''
        return self.rotation_dir

    def can_rotate(self, board):
        ''' Parameters: board - type: Board object
            Return value: type : bool
            
            Checks if the shape can be rotated.
            
            1. Get the rotation direction using the get_rotation_dir method
            2. Compute the position of each block after rotation and check if
            the new position is valid
            3. If any of the blocks cannot be moved to their new position,
            return False
                        
            otherwise all is good, return True
        '''
        #Get rotation direction from other method, and center
        rotation_direction = self.get_rotation_dir()
        center = self.center_block

        #For each block in list:
        for block in self.blocks:
            # Use these formulas to determine new coordinates (provided for us)
            x = center.x - rotation_direction*center.y + rotation_direction*block.y
            y = center.y + rotation_direction*center.x - rotation_direction*block.x
            # If these posistions are not valid on the board(other piece there
            #or out of bounds), return False
            if board.can_move(x, y) == False:
                return False
        return True
        
        
        

    def rotate(self, board):
        ''' Parameters: board - type: Board object

            rotates the shape:
            1. Get the rotation direction using the get_rotation_dir method
            2. Compute the position of each block after rotation
            3. Move the block to the new position
            
        '''    

        
        # For each block defined in shape
        for block in self.blocks:
            #Grab rotation direction and center block
            rotation_direction = self.get_rotation_dir()
            center = self.center_block
            #Compute new coordinates and call move method
            x = center.x - rotation_direction*center.y + rotation_direction*block.y
            y = center.y + rotation_direction*center.x - rotation_direction*block.x
            # Use x - block.x for dx, y-block.y for dy
            block.move(x - block.x, y - block.y)

        ### This should be at the END of your rotate code. 
        ### DO NOT touch it. Default behavior is that a piece will only shift
        ### rotation direciton after a successful rotation. This ensures that 
        ### pieces which switch rotations definitely remain within their 
        ### accepted rotation positions.
        if self.shift_rotation_dir:
            self.rotation_dir *= -1

        

############################################################
# ALL SHAPE CLASSES
############################################################

# For each shape in the game, we gave the coordinates for each block in the
# Tetronimo, using the center block as reference.  We then initialized a shape
# object with the list of coords and a color.  Self.center_block is used
# above for rotating; it tells us what the center block is
 
class I_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x - 2, center.y),
                  Point(center.x - 1, center.y),
                  Point(center.x    , center.y),
                  Point(center.x + 1, center.y)]
        Shape.__init__(self, coords, 'blue')
        self.shift_rotation_dir = True
        self.center_block = self.blocks[2]


class J_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x - 1, center.y),
                  Point(center.x    , center.y),
                  Point(center.x + 1, center.y),
                  Point(center.x + 1, center.y + 1)]
        Shape.__init__(self, coords, 'orange')
        self.center_block = self.blocks[1]


class L_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x - 1, center.y),
                  Point(center.x    , center.y),
                  Point(center.x + 1, center.y),
                  Point(center.x - 1, center.y + 1)]
        Shape.__init__(self, coords, 'cyan')
        self.center_block = self.blocks[1]


class O_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x    , center.y),
                  Point(center.x - 1, center.y),
                  Point(center.x   , center.y + 1),
                  Point(center.x - 1, center.y + 1)]
        Shape.__init__(self, coords, 'red')
        self.center_block = self.blocks[0]

    def rotate(self, board):
        # Override Shape's rotate method since O_Shape does not rotate
        return 



class S_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x    , center.y),
                  Point(center.x    , center.y + 1),
                  Point(center.x + 1, center.y),
                  Point(center.x - 1, center.y + 1)]
        Shape.__init__(self, coords, 'green')
        self.center_block = self.blocks[0]
        self.shift_rotation_dir = True
        self.rotation_dir = -1


class T_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x - 1, center.y),
                  Point(center.x    , center.y),
                  Point(center.x + 1, center.y),
                  Point(center.x    , center.y + 1)]
        Shape.__init__(self, coords, 'yellow')
        self.center_block = self.blocks[1]


class Z_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x - 1, center.y),
                  Point(center.x    , center.y), 
                  Point(center.x    , center.y + 1),
                  Point(center.x + 1, center.y + 1)]      
        Shape.__init__(self, coords, 'magenta')
        self.shift_rotation_dir = True
        self.rotation_dir = -1
        self.center_block = self.blocks[1]



############################################################
# BOARD CLASS
############################################################

class Board():
    ''' Board class: it represents the Tetris board

        Attributes: width - type:int - width of the board in squares
                    height - type:int - height of the board in squares
                    canvas - type:CanvasFrame - where the pieces will be drawn
                    grid - type:Dictionary - keeps track of the current state of
                    the board; stores the blocks for a given position
    '''
    
    def __init__(self, win, width, height):
        self.width = width
        self.height = height

        # create a canvas to draw the tetris shapes on
        self.canvas = CanvasFrame(win, self.width * Block.BLOCK_SIZE,
                                        self.height * Block.BLOCK_SIZE)
        self.canvas.setBackground('black')
        # Create Scoreboard with same width, but a height of 100 pixels
        self.scoreboard = Scoreboard(win, width, 100)

        # create an empty dictionary
        # currently we have no shapes on the board
        self.grid = {}

    def draw_shape(self, shape):
        ''' Parameters: shape - type: Shape
            Return value: type: bool

            draws the shape on the board if there is space for it
            and returns True, otherwise it returns False
        '''
        # If the shape can move function returns True, draw new shape
        if shape.can_move(self, 0, 0):
            shape.draw(self.canvas)
            return True
        # If not, no shape can be drawn (game over)
        else:
            self.game_over()

    def can_move(self, x, y):
        ''' Parameters: x - type:int
                        y - type:int
            Return value: type: bool

            1. check if it is ok to move to square x,y
            if the position is outside of the board boundaries, can't move there
            return False

            2. if there is already a block at that postion, can't move there
            return False

            3. otherwise return True
            
        '''
        # if this x, y coordinates are within the board and there are no pieces there (aka no keys
        # with the coordinates in the dictionary), return True
        if (x >= 0 and x < self.width) and (y >= 0 and y < self.height) and (x, y) not in self.grid.keys():
            return True
        return False
            
        pass

    def add_shape(self, shape):
        ''' Parameter: shape - type:Shape
            
            add a shape to the grid, i.e.
            add each block to the grid using its
            (x, y) coordinates as a dictionary key

            Hint: use the get_blocks method on Shape to
            get the list of blocks
            
        '''
        
        #For each block in a given shape, add it to the self.grid dictionary
        for block in shape.get_blocks():
            self.grid[(block.x, block.y)] = block


    def delete_row(self, y):
        ''' Parameters: y - type:int

            remove all the blocks in row y
            to remove a block you must remove it from the grid
            and erase it from the screen.
            If you dont remember how to erase a graphics object
            from the screen, take a look at the Graphics Library
            handout
            
        '''
        # If the row is complete (use is_row_complete method)
        if self.is_row_complete(y) == True:
            #For every key in the block dictionary,
            for item in self.grid.keys():
                # If the y coordinate of that key matches the row that must be removed 
                if item[1] == y:
                    #Undraw the item and delete it from the dictionary
                    self.grid[item].undraw()
                    del self.grid[item]
                    
    
    def is_row_complete(self, y):        
        ''' Parameter: y - type: int
            Return value: type: bool

            for each block in row y
            check if there is a block in the grid (use the in operator) 
            if there is one square that is not occupied, return False
            otherwise return True
            
        '''
        # Define empty dictionary to keep track of blocks in row
        y_list = []
        # for every block on the board, if it is in this row, append to list
        for block in self.grid.keys():
            if block[1] == y:
                y_list.append(block)
        

        # If the row is full (i.e. length of the list is the same as the width of the board)
        # empty the list and return True
        if len(y_list) == self.width:
            y_list = []
            return True
        return False

    
    def move_down_rows(self, y_start):
        ''' Parameters: y_start - type:int                        

            for each row from y_start to the top
                for each column
                    check if there is a block in the grid
                    if there is, remove it from the grid
                    and move the block object down on the screen
                    and then place it back in the grid in the new position

        '''
        # For each row from y_start to the top
        for row in range(y_start, 0, -1):
            # And each column on the board
            for column in range(0, self.width):
                # If there is a block there, move it down 1, delete from grid
                # and add new coordinates to the grid
                if (column, row) in self.grid.keys():
                    #print "WE MADE IT"
                    self.grid[(column, row)].move(0, 1)
                    block = self.grid[(column, row)]
                    del self.grid[(column, row)]
                    self.grid[(column, row + 1)] = block
    
    def remove_complete_rows(self):
        ''' removes all the complete rows
            1. for each row, y, 
            2. check if the row is complete
                if it is,
                    delete the row
                    move all rows down starting at row y - 1

        '''
        # Define empty list for keeping track of how many lines deleted(scoring purposes)
        lines_completed = []

        #For each row in the board, if it is complete, delete, move down rows,
        #Append the list
        for row in range(0, self.height):
            if self.is_row_complete(row) == True:
                #print "YADDA YADDA"
                self.delete_row(row)
                self.move_down_rows(row - 1)
                lines_completed.append('a')
        # Call the add_score method in the scoreboard class with the # of completed lines
        self.scoreboard.add_score(len(lines_completed))

    def game_over(self):
        ''' display "Game Over !!!" message in the center of the board
            HINT: use the Text class from the graphics library
        '''
        # Displays game_over message on screen
        game_over_message = Text(Point(150, 250), "GAME OVER \n BEETCHES")
        game_over_message.setStyle('bold')
        game_over_message.setSize(25)
        game_over_message.setTextColor('white')
        game_over_message.setFace('helvetica')
        game_over_message.draw(self.canvas)

            
############################################################
# SCOREBOARD CLASS
############################################################

class Scoreboard():

    
    def __init__(self, win, width, height):
        self.width = width
        self.height = height

        # create a canvas to draw the tetris shapes on
        self.canvas = CanvasFrame(win, self.width * Block.BLOCK_SIZE,
                                        100)
        self.canvas.setBackground('black')

        # Start the score off at 0, level off at 1
        self.current_score = 0
        self.current_level = 1

        # Text object displaying the Score
        self.score = Text(Point(75, 25), "Score: " + str(self.current_score))
        self.score.setStyle('bold')
        self.score.setSize(18)
        self.score.setTextColor('white')
        self.score.setFace('helvetica')

        # Text object displaying the Level
        self.levels = Text(Point(75, 50), "Level: " + str(self.current_level))
        self.levels.setStyle('bold')
        self.levels.setSize(18)
        self.levels.setTextColor('white')
        self.levels.setFace('helvetica')

        # Draw the Text objects on the screen
        self.score.draw(self.canvas)
        self.levels.draw(self.canvas)

        # Set the current_level = the method defined below
        self.current_level = self.increase_level()

    # This method is called from remove_complete_rows method, using len(lines_completed) as parameter
    def add_score(self, lines):
        # Depending on # of lines completed, add score accordingly
        if lines == 1:
            self.current_score += 100
        elif lines == 2:
            self.current_score += 300
        elif lines == 3:
            self.current_score += 450
        elif lines == 4:
            self.current_score += 700
        #Change Text Object
        self.score.setText("Score: "+ str(self.current_score))

    def increase_level(self):
        # Depending on Score, change level and text object
        while self.current_score <= 1000:
            self.current_level = 1
            self.levels.setText("Level: "+ str(self.current_level))
            return self.current_level
        while self.current_score > 1000 and self.current_score <= 5000:
            self.current_level = 2
            self.levels.setText("Level: "+ str(self.current_level))
            return self.current_level
        while self.current_score > 5000 and self.current_score <= 10000:
            self.current_level = 3
            self.levels.setText("Level: "+ str(self.current_level))
            return self.current_level
        while self.current_score > 10000 and self.current_score <= 15000:
            self.current_level = 4
            self.levels.setText("Level: "+ str(self.current_level))
            return self.current_level
        while self.current_score > 15000 and self.current_score <= 19000:
            self.current_level = 5
            self.levels.setText("Level: "+ str(self.current_level))
            return self.current_level
        while self.current_score > 19000 and self.current_score <= 23000:
            self.current_level = 6
            self.levels.setText("Level: "+ str(self.current_level))
            return self.current_level
        while self.current_score > 23000 and self.current_score <= 27000:
            self.current_level = 7
            self.levels.setText("Level: "+ str(self.current_level))
            return self.current_level
        while self.current_score > 27000 and self.current_score <= 30000:
            self.current_level = 8
            self.levels.setText("Level: "+ str(self.current_level))
            return self.current_level
        while self.current_score > 30000 and self.current_score <= 33000:
            self.current_level = 9
            self.levels.setText("Level: "+ str(self.current_level))
            return self.current_level
        while self.current_score > 33000:
            self.current_level = 10
            self.levels.setText("Level: "+ str(self.current_level))
            return self.current_level
        

############################################################
# TETRIS CLASS
############################################################

class Tetris():
    ''' Tetris class: Controls the game play
        Attributes:
            SHAPES - type: list (list of Shape classes)
            DIRECTION - type: dictionary - converts string direction to (dx, dy)
            BOARD_WIDTH - type:int - the width of the board
            BOARD_HEIGHT - type:int - the height of the board
            board - type:Board - the tetris board
            win - type:Window - the window for the tetris game
            delay - type:int - the speed in milliseconds for moving the shapes
            current_shapes - type: Shape - the current moving shape on the board
    '''
    
    SHAPES = [I_shape, J_shape, L_shape, O_shape, S_shape, T_shape, Z_shape]
    DIRECTION = {'Left':(-1, 0), 'Right':(1, 0), 'Down':(0, 1)}
    BOARD_WIDTH = 10
    BOARD_HEIGHT = 20
    
    def __init__(self, win):
        self.board = Board(win, self.BOARD_WIDTH, self.BOARD_HEIGHT)
        self.win = win
        self.delay = 1000 #ms

        # sets up the keyboard events
        # when a key is called the method key_pressed will be called
        self.win.bind_all('<Key>', self.key_pressed)

        # set the current shape to a random new shape
        self.current_shape = self.create_new_shape()

        # Draw the current_shape on the board (take a look at the
        # draw_shape method in the Board class)
        self.board.draw_shape(self.current_shape)

        # For Step 9:  animate the shape!
        self.animate_shape()
        
        

    def create_new_shape(self):
        ''' Return value: type: Shape
            
            Create a random new shape that is centered
             at y = 0 and x = int(self.BOARD_WIDTH/2)
            return the shape
        '''
        # Pick a random number from 0 to 6
        rand_shape = random.randint(0, 6)
        # That number corresponds to a shape in SHAPES list. Use coordinates to tell where to draw
        new_shape = self.SHAPES[rand_shape](Point(int(self.BOARD_WIDTH/2), 0))
        return new_shape
        
        pass
    
    def animate_shape(self):
        ''' animate the shape - move down at equal intervals
            specified by the delay attribute
        '''
        self.board.scoreboard.increase_level()
        #Depending onlevel, change the delay for animation to get shorter and shorter
        # move the shape down
        if self.board.scoreboard.current_level == 1:
            self.delay = 1000
            self.do_move('Down')
            self.win.after(self.delay, self.animate_shape)
        elif self.board.scoreboard.current_level == 2:
            self.delay = 900
            self.do_move('Down')
            self.win.after(self.delay, self.animate_shape)
        elif self.board.scoreboard.current_level == 3:
            self.delay = 800
            self.do_move('Down')
            self.win.after(self.delay, self.animate_shape)
        elif self.board.scoreboard.current_level == 4:
            self.delay = 650
            self.do_move('Down')
            self.win.after(self.delay, self.animate_shape)
        elif self.board.scoreboard.current_level == 5:
            self.delay = 500
            self.do_move('Down')
            self.win.after(self.delay, self.animate_shape)
        elif self.board.scoreboard.current_level == 6:
            self.delay = 400
            self.do_move('Down')
            self.win.after(self.delay, self.animate_shape)
        elif self.board.scoreboard.current_level == 7:
            self.delay = 300
            self.do_move('Down')
            self.win.after(self.delay, self.animate_shape)
        elif self.board.scoreboard.current_level == 8:
            self.delay = 200
            self.do_move('Down')
            self.win.after(self.delay, self.animate_shape)
        elif self.board.scoreboard.current_level == 9:
            self.delay = 100
            self.do_move('Down')
            self.win.after(self.delay, self.animate_shape)
        elif self.board.scoreboard.current_level == 10:
            self.delay = 50
            self.do_move('Down')
            self.win.after(self.delay, self.animate_shape)
        
    
    def do_move(self, direction):
        ''' Parameters: direction - type: string
            Return value: type: bool

            Move the current shape in the direction specified by the parameter:
            First check if the shape can move. If it can, move it and return True
            Otherwise if the direction we tried to move was 'Down',
            1. add the current shape to the board
            2. remove the completed rows if any 
            3. create a new random shape and set current_shape attribute
            4. If the shape cannot be drawn on the board, display a
               game over message

            return False

        '''
        # space bar is hit, move shape down until it can't move anymore
        if direction == 'space':           
            while self.current_shape.can_move(self.board, self.DIRECTION['Down'][0], self.DIRECTION['Down'][1]) == True:
                self.current_shape.move(self.DIRECTION['Down'][0], self.DIRECTION['Down'][1])
            # add new shape to grid, create new shape to draw, and check for completed rows
            self.board.add_shape(self.current_shape)
            self.current_shape = self.create_new_shape()
            self.board.draw_shape(self.current_shape)
            self.board.remove_complete_rows()
            
        #if the shape can move in the direction given by DIRECTION list, move it there       
        elif self.current_shape.can_move(self.board, self.DIRECTION[direction][0], self.DIRECTION[direction][1]) == True:
            self.current_shape.move(self.DIRECTION[direction][0], self.DIRECTION[direction][1])
            return True

        else:
            # if the shape can't  move any moore
            if direction == 'Down':
                # add new shape to grid, create new shape to draw, and check for completed rows
                self.board.add_shape(self.current_shape)
                self.current_shape = self.create_new_shape()
                self.board.draw_shape(self.current_shape)
                self.board.remove_complete_rows()
            return False
        

    def do_rotate(self):
        ''' Checks if the current_shape can be rotated and
            rotates if it can
        '''
        
        
        #If shape can rotate, rotate it
        if self.current_shape.can_rotate(self.board) == True:
            self.current_shape.rotate(self.board)
        
        
    
    def key_pressed(self, event):
        ''' this function is called when a key is pressed on the keyboard
            it currenly just prints the value of the key

            Modify the function so that if the user presses the arrow keys
            'Left', 'Right' or 'Down', the current_shape will move in
            the appropriate direction

            if the user presses the space bar 'space', the shape will move
            down until it can no longer move and is added to the board

            if the user presses the 'Up' arrow key ,
                the shape should rotate.

        '''
            
        
        key = event.keysym
        # If key is up, call do_rotate function
        if key == 'Up':
            self.do_rotate()
        
        # Else, call do_move function
        else:
            self.do_move(key)


       
################################################################
# Start the game
################################################################

win = Window("Tetris")
game = Tetris(win)
win.mainloop()
