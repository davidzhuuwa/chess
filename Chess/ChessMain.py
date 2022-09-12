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
    loadImages() # only do this once, before the while loop 
    print(gs.board)
    isRunning = True
    
    while isRunning:
        for e in p.event.get():
            if e.type == p.QUIT:
                isRunning = False 
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
    