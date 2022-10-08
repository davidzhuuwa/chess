"""
Main driver file. It will be responsible for handling user input and displaying the current GameState object.
"""

import pygame as p 
import ChessEngine

p.init()
WIDTH = HEIGHT = 512 # 400 is another option
DIMENSION = 8 #dimensions of a chess board are 8x8
SQ_SIZE = HEIGHT // DIMENSION 
MAX_FPS = 15 # for animations later on 
IMAGES = {} # only want to load them in one time 

'''
Initialise a global dictionary of images. This will be called exactly once in the main
'''
#nice!
def loadImages():
    """
    Loading images for the chess set
    """
    pieces = ['wp','wR','wN','wB','wQ','wK','bp','bR','bN','bB','bK','bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load(f"Chess/images/{piece}.png"),(SQ_SIZE,SQ_SIZE))
    # Note we can acess an image by saying 'IMAGES['wp']'
    
    

def main():
    """ The main driver for our code. This will handle user input and updating the graphics
    """
    screen = p.display.set_mode((WIDTH,HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("White"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False # flag variable for when a move is made 
    loadImages() # only do this once, before the while loop 
    #print(gs.board)
    isRunning = True
    sqSelected = () #no square is selected, keep track of last click of user (tuple: (row,col))
    playerClicks = [] # list of up to two elements, keep track of player clicks (Two tuples: [(6,4), (4,4)])
    
    while isRunning:
        for e in p.event.get():
            if e.type == p.QUIT:
                isRunning = False 
            # mouse handler
            elif e.type == p.MOUSEBUTTONDOWN: # TODO: CLICK AND DRAG AS WELL LATER 
                location = p.mouse.get_pos() # (x, y) location of the mouse 
                col = location[0]//SQ_SIZE  # // double divide for rounding
                row = location[1]//SQ_SIZE
                # check if user previously selected this square 
                if sqSelected == (row, col): # the user clicked the same square twice
                    sqSelected = () # deselect the selected square
                    playerClicks = []
                else:
                    sqSelected = (row, col) 
                    playerClicks.append(sqSelected)
                if len(playerClicks) == 2: # after 2nd click 
                    # make the chess move now and keep track of the move
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1],gs.board)
                    print(move.getChessNotation())
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                    sqSelected = () # reset user clicks 
                    playerClicks = []
            # key handlers 
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: # undo when 'z' is pressed 
                    gs.undoMove()
                    moveMade = True
        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False  
                      
        drawGameState(screen,gs)
        clock.tick(MAX_FPS)
        p.display.flip()


def drawGameState(screen,gs):
    """ Responsible for all graphics within a current game state

    Args:
        screen (_type_): _description_
        gs (_type_): _description_
    """
    drawBoard(screen) # draws the squares on the board 
    # TODO: add in piece highlighting, move suggestions e.g. here 
    drawPieces(screen,gs) # draw pieces on top of the squares 
    
    
def drawBoard(screen):
    """ Draws the squares on the board. The top left square is always light

    Args:
        screen (_type_): _description_
    """
    colors = [p.Color("white"),p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c)%2)] # even = white, #odd = grey 
            p.draw.rect(screen,color,p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))
             
def drawPieces(screen,gs):
    """Draw the pieces on the board using the current GameState.board

    Args:
        screen (_type_): _description_
        gs (_type_): _description_
    """
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = gs.board[r][c]
            if piece != "--": # not an empty square 
                screen.blit(IMAGES[piece],p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))
                
    
if __name__ == "__main__":    
    main()
    