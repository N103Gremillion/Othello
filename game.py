import pygame;
from board import Board;
from menu import Menu;
from player import Player;

grey = (128, 128, 128)
black = (0, 0, 0)
white = (255, 255, 255)

class Game:

    def __init__(self):
        self.curScreen = "menu"
        self.board = Board(435, 490, grey)
        self.menu = Menu(435, 490)
        self.player1 = Player(1, "black")
        self.player2 = Player(2, "white")
        self.curPlayer = self.player1
    
    def startGame(self):

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    self.handleBoardClick()
                    self.handleMenuClick()
                if event.type == pygame.KEYDOWN:
                    self.handleKeyPress(event.key)
                if event.type == pygame.QUIT:
                    running = False  

            pygame.display.flip()

    def openMenu(self):
        self.curScreen = "menu"

    def closeMenu(self):    
        self.curScreen = "board"

    def handleMenuClick(self):
        if (self.curScreen == "board"):
            return
    
    def handleKeyPress(self, key):
        if (key == pygame.K_ESCAPE):
            if (self.curScreen == "menu"):
                self.closeMenu()
                self.board.drawBoard(grey)
                self.board.drawCurBoard()
                self.board.highlightValidPositions()
            elif (self.curScreen == "board"):
                self.openMenu()
                self.menu.drawMenu()

    def handleBoardClick(self):
        if (self.curScreen == "menu"):
            return
        
        pos = pygame.mouse.get_pos()
        x, y = pos
        piecePlaced = self.board.placePieceUsingPosition(x, y, self.curPlayer.playerNumber)

        if piecePlaced:
            
            positionPlace = self.board.getIndeciesWithPosition(x, y)
            self.updateBoard(positionPlace)
            self.renderBoard(positionPlace)
           
    def updateBoard(self, postion):
        x, y = postion
        self.board.updateGrid(self.curPlayer.playerNumber, x, y)
        self.board.validMoves = self.getValidPlacements()
        self.tallyScore()
    
    def renderBoard(self, position):
        x, y = position
        self.board.clearBoardVisuals()
        self.board.drawCurBoard()
        self.board.updateCurrentTurnText(self.curPlayer.playerNumber)
        self.board.highlightValidPositions()
        self.board.renderNewScores(self.player1.score, self.player2.score)

    def tallyScore(self):
        self.player1.score = 0
        self.player2.score = 0
        grid = self.board.grid

        for i in range(len(grid)):
            for j in range(len(grid[0])):
                # P1 of black
                if (grid[i][j] == 1):
                    self.player1.score += 10
                elif (grid[i][j] == 2):
                    self.player2.score += 10

    def getValidPlacements(self):
        
        # player nums and current state of the board | validIndexes is a list of tuples for valid move indexes
        self.directionsFilledWithPlacement = []
        
        p1 = 1
        p2 = 2
        grid = self.board.grid
        curPlayer = self.curPlayer
        validIndexes = []
        
        # get previous players turn and to try and search for oposing player positions | reminder: p1 = black = 1 on grid / p2 = white = 2 on grid
        if curPlayer.playerNumber == 1:
            curPlayer = self.player2
        else:
            curPlayer = self.player1
        
        # search for the valid positions for curPlayer
        for row in range(len(grid)):
            for col in range(len(grid[0])):
                curNum = grid[row][col]
                if (curNum == 0 and self.isIndexPlacable(row, col, grid, curPlayer.playerNumber)):
                    validIndexes.append((row + 1, col + 1))
              
        # if none of the position where valid for the previous player flip back and try the other
        if len(validIndexes) > 0:
            self.curPlayer = curPlayer
            return validIndexes
        
        curPlayer = self.curPlayer
        
        for row in range(len(grid)):
            for col in range(len(grid[0])):
                curNum = grid[row][col]
                if (curNum == 0 and self.isIndexPlacable(row, col, grid, curPlayer.playerNumber)):
                    validIndexes.append((row, col))

        return validIndexes

    def isIndexPlacable(self, x, y, grid, colorChecking):
        empty = 0
        black = 1
        white = 2
        
        if grid[x][y] != empty:
            return False
        
        # Set opponent's color
        opponentColor = black if colorChecking == white else white

        # Directions to check around the placement
        directions = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
        isPlaceable = False

        for dx, dy in directions:
            newX, newY = x + dx, y + dy
            
            # Check bounds
            if 0 <= newX < 8 and 0 <= newY < 8:
                if grid[newX][newY] == opponentColor:
                    if self.checkForSandwich(grid, opponentColor, (dx, dy), newX, newY):
                        # Only set isPlaceable to True after confirming the sandwich
                        isPlaceable = True

        return isPlaceable

    def checkForSandwich(self, grid, colorBeingSandwiched, direction, x, y):
        empty = 0
        black = 1
        white = 2

        # Determine closing color
        closingColor = black if colorBeingSandwiched == white else white

        dx, dy = direction
        newX, newY = x + dx, y + dy

        # Check the line in the specified direction
        while 0 <= newX < 8 and 0 <= newY < 8:
            if grid[newX][newY] == empty:
                return False
            if grid[newX][newY] == closingColor:
                # A closing color was found // sandwich confirmed in this direction
                return True
            
            # Move further in the current direction
            newX += dx
            newY += dy
        
        return False
                
        
        