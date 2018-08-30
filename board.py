from graphics import Text, Point, CanvasFrame, Line
from block import Block


class Board:
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

        # set the var that defines how much speed should increase
        self.delta_delay = 0
        self.board_delay = 2000  # ms

        # create a canvas to draw the tetris shapes on
        self.canvas = CanvasFrame(win, self.width * Block.BLOCK_SIZE * 2,
                                  self.height * Block.BLOCK_SIZE)
        self.canvas.setBackground('light gray')

        # draw a vertical line to separate gaming part from info part
        line = Line(Point(self.width * Block.BLOCK_SIZE, 0), \
                    Point(self.width * Block.BLOCK_SIZE, self.height * Block.BLOCK_SIZE))
        line.draw(self.canvas)

        # display rules of the game
        rules = Text(Point(self.canvas.getWidth() / 1.35, self.canvas.getHeight() / 1.5), \
                     '        INSTRUCTIONS :            \n\n' + \
                     '   <- | ->  arrows to move         \n' + \
                     '     "up" arrow to rotate               \n' + \
                     '   "down" arrow to move down\n' + \
                     '       "space" to drop                      \n' + \
                     '        "p" to pause                           \n' + \
                     '        "s" to resume                         \n' + \
                     '   "d" to show debug info          \n\n' + \
                     '        SCORING :                       \n\n' + \
                     '     1   point   - 1 row                   \n' + \
                     '     4   points - 2 rows                  \n' + \
                     '     9   points - 3 rows                  \n' + \
                     '    16   points - 4 rows                  \n')
        rules.draw(self.canvas)

        # set up score counter and text holder for it
        self.score = 0
        self.score_text = Text(Point(self.canvas.getWidth() / 1.35, \
                                     self.canvas.getHeight() / 3), 'SCORE : ' + str(self.score))
        self.score_text.draw(self.canvas)

        # speed to display
        self.speed = self.board_delay - self.delta_delay
        self.speed_text = Text(Point(self.canvas.getWidth() / 1.35, \
                                     self.canvas.getHeight() / 3.5), 'DROP DOWN DELAY ms : ' + \
                               str(self.speed))
        self.speed_text.draw(self.canvas)

        # file handle to read and write best result
        self.result_file = self.read_best_result()

        # best_score and best speed so far
        if (self.result_file is not None):
            lines = self.result_file.readlines()

            self.best_score = int(lines[0])
            self.best_speed = int(lines[1])
        else:
            self.best_score = 0
            self.best_speed = 0

        # create an empty dictionary
        # currently we have no shapes on the board
        self.grid = {}

    def draw_shape(self, shape):
        ''' Parameters: shape - type: Shape
            Return value: type: bool

            draws the shape on the board if there is space for it
            and returns True, otherwise it returns False
        '''
        if shape.can_move(self, 0, 0):
            shape.draw(self.canvas)
            return True
        return False

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
        if x < 0 or x > self.width - 1 or y < 0 or y > self.height - 1 or (x, y) in self.grid.keys():
            return False
        else:
            return True

    def add_shape(self, shape):
        ''' Parameter: shape - type:Shape
            add a shape to the grid, i.e.
            add each block to the grid using its
            (x, y) coordinates as a dictionary key
        '''
        for block in shape.get_blocks():
            self.grid[(block.x, block.y)] = block

    def update_delay(self):
        ''' update drop down delay '''
        self.speed = self.board_delay - self.delta_delay
        self.speed_text.undraw()
        self.speed_text = Text(Point(self.canvas.getWidth() / 1.35, \
                                     self.canvas.getHeight() / 3.5), 'DROP DOWN DELAY ms : ' + \
                               str(self.speed))
        self.speed_text.draw(self.canvas)

    def update_score(self, n):
        ''' Parameters: n - type: int
           update the score based on the number of
           rows deleted in one move
        '''
        # update score value
        if n == 1:
            self.score += 1
        elif n == 2:
            self.score += 4
        elif n == 3:
            self.score += 9
        elif n == 4:
            self.score += 16
        # update score text
        self.score_text.undraw()
        self.score_text = Text(Point(self.canvas.getWidth() / 1.35, \
                                     self.canvas.getHeight() / 3), 'SCORE : ' + str(self.score))
        self.score_text.draw(self.canvas)

    def delete_row(self, y):
        ''' Parameters: y - type:int
            remove all the blocks in row y
            to remove a block you must remove it from the grid
            and erase it from the screen.
        '''
        for x in range(0, self.width):
            self.grid[(x, y)].undraw()
            del self.grid[(x, y)]

    def is_row_complete(self, y):
        ''' Parameter: y - type: int
            Return value: type: bool

            for each block in row y
            check if there is a block in the grid (use the in operator)
            if there is one square that is not occupied, return False
            otherwise return True
        '''
        for x in range(0, self.width):
            if (x, y) not in self.grid:
                return False
        return True

    def move_down_rows(self, y_start):
        ''' Parameters: y_start - type:int
            for each row from y_start to the top
                for each column
                    check if there is a block in the grid
                    if there is, remove it from the grid
                    and move the block object down on the screen
                    and then place it back in the grid in the new position
        '''
        y = y_start
        while y >= 0:
            for x in range(0, self.width):
                if (x, y) in self.grid:
                    tb = self.grid[(x, y)]
                    self.grid[(x, y)].undraw()
                    del self.grid[(x, y)]
                    self.grid[(x, y + 1)] = Block(Point(tb.x, tb.y + 1), tb.color)
                    self.grid[(x, y + 1)].draw(self.canvas)
            y -= 1

    def remove_complete_rows(self):
        ''' removes all the complete rows
            1. for each row, y,
            2. check if the row is complete
                if it is,
                    update complete rows counter
                    delete the row
                    move all rows down starting at row y - 1
               update score
        '''
        complete_rows = 0
        for y in range(0, self.height):
            if self.is_row_complete(y):
                complete_rows += 1
                self.delete_row(y)
                self.move_down_rows(y - 1)
        self.update_score(complete_rows)
        # increase speed
        if (complete_rows != 0):
            self.delta_delay += self.score
            self.update_delay()

    def game_over(self):
        ''' display "Game Over" message in the center of the board
             use the Text class from the graphics library
        '''
        gg = Text(Point(self.canvas.getWidth() / 2, self.canvas.getHeight() / 2), 'GAME OVER')
        gg.draw(self.canvas)
        self.save_result()

    def save_result(self):
        ''' save current score and drop down speed in a champion.txt file'''
        if (self.score > self.best_score):
            self.result_file = self.read_best_result()
            self.result_file.truncate(0)  # erase file info
            self.result_file.write(str(self.score) + '\n' + str(self.speed))
            self.result_file.close()
            congrats = Text(Point(self.canvas.getWidth() / 4, self.canvas.getHeight() / 4), 'CONGRATULATIONS\n' + \
                            'YOU ARE THE NEW CHAMPION\nprevious best result: \nscore = %d\n speed = %d' % \
                            (self.best_score, self.best_speed))
            congrats.draw(self.canvas)
        else:
            self.result_file.close()

    def read_best_result(self):
        ''' read previous result to determine if current result is better and
            needs to be saved'''
        try:
            r_file = open('./champion.txt', 'r+')
        except IOError, e:
            print 'file open error :', e
            return None
        return r_file
