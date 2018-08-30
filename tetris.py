from shapes import *
from board import Board
from graphics import Text, Window
from random import random


class Tetris:
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
    DIRECTION = {'Left': (-1, 0), 'Right': (1, 0), 'Down': (0, 1)}
    BOARD_WIDTH = 10
    BOARD_HEIGHT = 20
    onPause = False

    def __init__(self, win):
        self.board = Board(win, self.BOARD_WIDTH, self.BOARD_HEIGHT)
        self.win = win
        self.delay = self.board.board_delay  # ms

        # sets up the keyboard events
        # when a key is called the method key_pressed will be called
        self.win.bind_all('<Key>', self.key_pressed)

        # create next shape to be displayed
        self.next_shape = self.create_new_shape()

        # set the current shape to a random new shape
        self.current_shape = self.create_new_shape()

        # Draw the current_shape oan the board (take a look at the
        # draw_shape method in the Board class)
        self.board.draw_shape(self.current_shape)
        self.animate_shape()

        # initialize pause text for later use when p is pressed
        self.pause = Text(Point(self.board.canvas.getWidth() / 4, \
                                self.board.canvas.getHeight() / 2), 'PAUSE')

    def create_new_shape(self):
        ''' Return value: type: Shape
            
            Create a random new shape that is centered
             at y = 0 and x = int(self.BOARD_WIDTH/2)
            return the shape
        '''
        # pick a random number from the SHAPES list attribute of the tetris class
        # create new shape
        return random.choice(self.SHAPES)(Point(int(self.BOARD_WIDTH / 2), 0))

    def animate_shape(self):
        ''' animate the shape - move down at equal intervals
            specified by the delay attribute
        '''
        if not self.onPause:
            self.do_move('Down')
            self.win.after(self.delay - self.board.delta_delay, self.animate_shape)

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
        tup = self.DIRECTION[direction]
        dx = tup[0]
        dy = tup[1]
        if self.current_shape.can_move(self.board, dx, dy):
            self.current_shape.move(dx, dy)
            return True
        elif tup == (0, 1):
            self.board.add_shape(self.current_shape)
            self.current_shape = self.next_shape
            self.next_shape = self.create_new_shape()
            if self.board.draw_shape(self.current_shape):
                self.board.remove_complete_rows()
            else:
                self.board.game_over()
        else:
            return False

    def do_rotate(self):
        ''' Checks if the current_shape can be rotated and
            rotates if it can
        '''

        ###        print 'can we rotate?', self.current_shape.can_rotate(self.board)
        if self.current_shape.can_rotate(self.board):
            self.current_shape.rotate(self.board)

    def key_pressed(self, event):
        ''' this function is called when a key is pressed on the keyboard

            if the user presses the arrow keys
            'Left', 'Right' or 'Down', the current_shape will move in
            the appropriate direction

            if the user presses the space bar 'space', the shape will move
            down until it can no longer move and is added to the board

            if the user presses the 'Up' arrow key ,
                the shape should rotate.

        '''
        # key is used to get the coordianates dx and dy to be used in the do_move method
        key = event.keysym
        # print key
        if key == 'Up':
            if not self.onPause:
                self.do_rotate()
            return
        elif key == 'space':
            if not self.onPause:
                while self.do_move('Down'):
                    {}
        elif key == 'p':
            self.onPause = True
            self.pause.draw(self.board.canvas)

        elif key == 'd':
            iter = self.board.grid.iterkeys()
            for pair in sorted(iter):
                print pair,
            print
        elif key == 's':
            self.onPause = False
            self.pause.undraw()
            self.animate_shape()
        else:
            if not self.onPause:
                self.do_move(key)


################################################################
# Start the game
################################################################

win = Window("Tetris")
game = Tetris(win)
win.mainloop()
