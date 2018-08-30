from block import Block


class Shape:
    ''' Shape class:
        Base class for all the tetris shapes
        Attributes: blocks - type: list - the list of blocks making up the shape
                    rotation_dir - type: int - the current rotation direction of the shape
                    shift_rotation_dir - type: Boolean - whether or not the shape rotates
    '''

    def __init__(self, coords, color):
        self.blocks = []
        self.rotation_dir = 1
        ### A boolean to indicate if a shape shifts rotation direction or not.
        ### Defaults to false since only 3 shapes shift rotation directions (I, S and Z)
        self.shift_rotation_dir = False

        for pos in coords:
            self.blocks.append(Block(pos, color))

    def get_blocks(self):
        '''
           returns the list of blocks
        '''
        return self.blocks

    def draw(self, win):
        ''' Parameter: win - type: CanvasFrame

            Draws the shape:
            i.e. draws each block
        '''
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

        # since a shape is a collection of blocks all we need to do
        # is to check if every block in the shape can be moved
        # since we already implemented block.can_move method
        # this should be easy
        shape_blocks = self.blocks

        for block in shape_blocks:
            if not block.can_move(board, dx, dy):
                return False
            else:
                continue
        return True

    def get_rotation_dir(self):
        ''' Return value: type: int

            returns the current rotation direction
        '''
        #        print 'get_rotation_dir returned', self.rotation_dir
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

        # for each block in a shape we calculate new x and y
        # than check if it is within bounds
        shape_blocks = self.blocks

        for block in shape_blocks:
            direc = self.get_rotation_dir()
            new_x = self.blocks[1].x - direc * self.blocks[1].y + direc * block.y
            new_y = self.blocks[1].y + direc * self.blocks[1].x - direc * block.x
            if not board.can_move(new_x, new_y):
                return False
            else:
                continue
        return True

    def rotate(self, board):
        ''' Parameters: board - type: Board object

            rotates the shape:
            1. Get the rotation direction using the get_rotation_dir method
            2. Compute the position of each block after rotation
            3. Move the block to the new position

        '''

        direc = self.get_rotation_dir()
        # print 'rotation dir',direc
        shape_blocks = self.blocks
        # print self.can_rotate(board)
        if self.can_rotate(board):
            for block in shape_blocks:
                new_x = self.blocks[1].x - direc * self.blocks[1].y + direc * block.y
                dx = new_x - block.x
                new_y = self.blocks[1].y + direc * self.blocks[1].x - direc * block.x
                dy = new_y - block.y
                # print 'dx ', dx, '  || dy ', dy
                block.move(dx, dy)

        ### DO NOT touch it. proven to be in working order
        if self.shift_rotation_dir:
            self.rotation_dir *= -1
