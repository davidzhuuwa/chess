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
        self.moveFunctions = {'p' : self.getPawnMoves,
                              'R' : self.getRookMoves,
                              'N' : self.getKnightMoves,
                              'B' : self.getBishopMoves,
                              'Q' : self.getQueenMoves,
                              'K' : self.getKingMoves}
        self.whiteToMove = True
        self.moveLog = [] 
        
        # Need to keep track of castling in the future as well 
    def makeMove(self, move):
        """ Takes a move as a parameter and executes it. Note this will not work for castling, en-passant, and pawn promotion

        Args:
            move (_type_): _description_
        """
        # assumes move is already valid 
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) # log the move so we can undo it later 
        self.whiteToMove = not self.whiteToMove # swap players
        
    def undoMove(self):
        """Undo the last move made.

        Returns:
            _type_: _description_
        """
        if len(self.moveLog) !=0: # make sure there is a move to undo
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove # swap players
            
    def getValidMoves(self):
        """Get all moves including checks (i.e. filters out illegal moves)
        - for each possible move, check to see if it is valid by:
            - making the move 
            - generate all possible moves for opposing player 
            - see if any of the moves can capture/attack your king 
            - if your king is safe, it is a valid move and add it to the list
        Returns:
            _type_: _description_
        """
        return self.getAllPossibleMoves() # for now we will not worry about checks
    
    def getAllPossibleMoves(self):
        """Get all possible moves without checks (i.e. including illegal moves that end in check)

        Returns:
            _type_: _description_
        """
        moves = []
        for r in range(len(self.board)): # number of rows
            for c in range(len(self.board[r])): # number of column in given rows
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn =='b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r,c,moves) # calls appropriate move function based on piece type
        return moves
                        
    def getPawnMoves(self, r, c, moves):
        """Get all the pawn moves for the pawn located at row, col and add these moves to the list

        Args:
            r (_type_): _description_
            c (_type_): _description_
            moves (_type_): _description_

        Returns:
            _type_: _description_
        """
        # Pawns can't move backwards, and white and black pawns move in different directions. Can also move two squares on their first moves, and can capture diagonally if a piece is there.
        # White pawns start on row 6
        # Black pawns start on row 1 
        # Assuming they're not blocked, can move one or two squares forward on their starting squares
        if self.whiteToMove: # white pawn moves
            if self.board[r-1][c] == '--': #1-square pawn advance
                moves.append(Move((r,c),(r-1,c),self.board))
                # Check if it is in starting position
                if r == 6 and self.board[r-2][c] == '--': #2-square pawn advance
                    moves.append(Move((r,c),(r-2,c),self.board))
            if c-1 >=0:
                # Can't capture off the left side of the board
                # Captures to the left
                if self.board[r-1][c-1][0] == 'b': # Enemy piece to capture
                    moves.append(Move((r,c),(r-1,c-1),self.board))
            if c+1 < 7:
                # Can't capture off the right side of the board
                # Captures to the right
                if self.board[r-1][c+1][0] == 'b': # Enemy piece to capture
                    moves.append(Move((r,c),(r-1,c+1),self.board))
        
        if not self.whiteToMove: # Black pawn moves        
            if self.board[r+1][c] == '--': # 1-square pawn advance
                moves.append(Move((r,c),(r+1,c),self.board))
                # Check if it is in starting position
                if r==1 and self.board[r+2][c] == '--': # 2-square pawn advance
                    moves.append(Move((r,c),(r+2,c),self.board)) 
            if c-1 >=0:
                # Captures to the left 
                if self.board[r+1][c-1][0] == 'w':
                    moves.append(Move((r,c),(r+1,c-1),self.board))
            if c+1 < 7:
                # Captures to the right 
                if self.board[r+1][c+1][0] == 'w':
                    moves.append(Move((r,c),(r+1,c+1),self.board))
                      
        return moves
        
    def getRookMoves(self, r, c, moves):
        """Get all the rook moves for the rook located at row, col and add these moves to the list 

        Args:
            r (_type_): _description_
            c (_type_): _description_
            moves (_type_): _description_

        Returns:
            _type_: _description_
        """
        # for each direction, check if you hit the edge of the board, or another piece
        # if you hit another piece, is it an enemy or a friendly piece
        
        directions = [(-1,0),(0,1),(1,0),(0,-1)]
        enemyColour = "b" if self.whiteToMove else "w"
        
        for d in directions:
            for i in range(1,8):
                endRow = r + d[0]*i
                endCol = c + d[1]*i
                if 0 <= endRow < 8 and 0 <= endCol < 8: # on board 
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--": # empty space valid 
                        moves.append(Move((r,c),(endRow,endCol),self.board))
                    elif endPiece[0] == enemyColour: # enemy piece is  valid
                        moves.append(Move((r,c),(endRow,endCol),self.board))
                        break 
                    else: # friendly piece invalid 
                        break 
                else: # off board 
                    break 
                            
    def getKnightMoves(self,r,c,moves):
        pass
    
    def getBishopMoves(self,r,c,moves):
        directions = [(-1,-1),(1,1),(-1,1),(1,-1)]
        enemyColour = "b" if self.whiteToMove else "w"
        
        for d in directions: 
            for i in range(1,8):
                endRow = r + d[0]*i
                endCol = c + d[1]*i
                if 0<= endRow <8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == '--':
                        moves.append(Move((r,c),(endRow,endCol),self.board))
                    elif endPiece[0] == enemyColour: # enemy piece is valid 
                        moves.append(Move((r,c),(endRow,endCol),self.board))
                        break 
                    else: # friendly piece invalid 
                        break 
                else: # off board
                    break 
    
    def getQueenMoves(self,r,c,moves):
        self.getRookMoves(r,c,moves)
        self.getBishopMoves(r,c,moves)
    
    def getKingMoves(self,r,c,moves):
        directions = [(-1,1),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,-1),(1,0)]
        enemyColour = "b" if self.whiteToMove else "w"
        
        for d in directions: 
            for i in range (1,2):
                endRow = r + d[0]*i
                endCol = c + d[1]*i
                if 0 <= endRow < 8 and 0 <= endCol < 8: 
                    endPiece = self.board[endRow][endCol]
                    if endPiece == '--': 
                        moves.append(Move((r,c),(endRow,endCol),self.board))
                    elif endPiece[0] == enemyColour: # enemy piece is valid 
                        moves.append(Move((r,c),(endRow,endCol),self.board))
                        break 
                    else: # friendly piece is invalid 
                        break 
                else: # off board 
                    break 
                
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
        self.moveID = self.startRow*1000 + self.startCol*100 + self.endRow*10 + self.endCol
        
    def __eq__(self,other):
        """Overriding the equals method

        Args:
            other (_type_): _description_
        """
        if isinstance(other,Move):
            return self.moveID == other.moveID 
        return False
            
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
        
        
        
        
        
        
        