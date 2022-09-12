"""
This class is responsible for storing all the information about the current state of a chess game. It's also responsible for determining the valid moves at the current state. It will also keep a move log.
"""

class GameState():
    def __init__(self):
        # Board is an 8x8 2D list. Each element of the list has two characters. 
        # The first character represents the colour of the piece, 'b' or 'w'
        # The second character represents the type of the piece, 'K', 'Q', 'R', 'B', 'N' or 'p'
        # The string "--" represents an empty space with no piece.
        self.board = [
            ["bR","bN","bB","bQ","bK","bB","bN","bR"],
            ["bp","bp","bp","bp","bp","bp","bp","bp"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],            
            ["--","--","--","--","--","--","--","--"],            
            ["--","--","--","--","--","--","--","--"],
            ["wp","wp","wp","wp","wp","wp","wp","wp"],
            ["wR","wN","wB","wQ","wK","wB","wN","wR"]
        ]
        self.whiteToMove = True
        self.moveLog = [] 
        
        # Need to keep track of castling in the future as well 
    def makeMove(self, move):
        # assumes move is already valid 
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) # log the move so we can undo it later 
        self.whiteToMove = not self.whiteToMove # swap players
        
class Move():
    # maps keys to values 
    # key : value 
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, 
                   "5": 3, "6": 2, "7": 1, "8": 0,}
    rowsToRanks = {v: k for k, v in ranksToRows.items()} #reversing a dictionary
    filesToCols = {"a": 0,"b": 1,"c": 2,"d": 3,"e": 4,
                   "f": 5,"g": 6,"h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}
    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        
    def getChessNotation(self):
        # add to make this like real chess notation
        notation = ""
        if self.pieceCaptured == '--' and self.pieceMoved[1]!='p':
            notation = self.pieceMoved[1]+ self.getRankFile(self.endRow,self.endCol)
        elif self.pieceCaptured == '--' and self.pieceMoved[1]=='p':
            notation = self.getRankFile(self.endRow,self.endCol)
        elif self.pieceCaptured != '--' and self.pieceMoved[1]!='p':
            notation = self.pieceMoved[1]+'x'+self.getRankFile(self.endRow,self.endCol)
        elif self.pieceCaptured != '--' and self.pieceMoved[1]=='p':
            notation = self.getRankFile(self.startRow,self.startCol)[0] +'x'+self.getRankFile(self.endRow,self.endCol)
        return notation
 
    def getRankFile(self,r,c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
        
        
        
        
        
        
        