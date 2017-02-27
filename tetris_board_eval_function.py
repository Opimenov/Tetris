# tetris game contains a board
# board contains grid - type: Dictionary - keeps track of the current state
# of the board; stores the blocks for a given position
# each block has: int x, y specifies the position on the tetris board in terms 
# of the square grid
#############################################################
# BOT CLASS
#############################################################

class Bot():
    ''' Bot class:
       implements a player for the tetris game
       Attributes: bot_name : String
   '''
    def __init__(self, bot_name):
        self.bot_name = bot_name

        
    def evaluate_state(self, grid):
        ''' Parameters: grid - dictionary of all the blocks on the board 
        thougths about implementation:
        get the number of complete horizontal rows first
        then look at incomplete rows (might add all blocks in a row and give more 
        value to rows that are more complete)
        returns value type : int
        '''
        
        pass

        
    def find_a_position_for_current_shape(self, board, current_shape):
        ''' Parameters: board - dictionary of blocks
                              current_shape - is one of the shapes defined in all 
                                                      shapes in tetris.py
        to do this we need to:
            - for each leagal position calculate the score
            - keep track of the max score 
            - return position that produces the state with the max score
        '''
        pass
