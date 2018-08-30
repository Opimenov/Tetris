from graphics import Rectangle, Point


class Block(Rectangle):
    ''' Block class:
        Implement a block for a tetris piece
        Attributes: x - type: int
                    y - type: int
        specify the position on the tetris board
        in terms of the square grid
    '''

    BLOCK_SIZE = 30
    OUTLINE_WIDTH = 1

    def __init__(self, pos, color):
        self.x = pos.x
        self.y = pos.y
        self.color = color

        p1 = Point(pos.x * Block.BLOCK_SIZE + Block.OUTLINE_WIDTH,
                   pos.y * Block.BLOCK_SIZE + Block.OUTLINE_WIDTH)
        p2 = Point(p1.x + Block.BLOCK_SIZE, p1.y + Block.BLOCK_SIZE)

        Rectangle.__init__(self, p1, p2)
        self.setWidth(Block.OUTLINE_WIDTH)
        self.setFill(color)

    def can_move(self, board, dx, dy):
        ''' Parameters: dx - type: int
                        dy - type: int

            Return value: type: bool

            checks if the block can move dx squares in the x direction
            and dy squares in the y direction
            Returns True if it can, and False otherwise
        '''

        new_x = self.x + dx
        new_y = self.y + dy
        return board.can_move(new_x, new_y)

    def move(self, dx, dy):
        ''' Parameters: dx - type: int
                        dy - type: int

            moves the block dx squares in the x direction
            and dy squares in the y direction
        '''

        self.x += dx
        self.y += dy

        Rectangle.move(self, dx * Block.BLOCK_SIZE, dy * Block.BLOCK_SIZE)
