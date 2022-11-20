# imports
import copy
import time


# global variables

# classes


# Board
# sudoko board, made up of tiles 9x9
class Board:
    # constructor
    def __init__(self, startingState):
        # instance variables
        # board is the overall sudoko board
        self.startingState = startingState
        self.board = []
        # initialize the board, setting all to - to signify a blank space
        for x in range(9):
            for y in range(9):
                self.board.append(Tile(x + 1, y + 1, self.determineBlockID(x + 1, y + 1), '-'))
        # set the initial tiles based on the provided startingState
        self.setStartingTiles()

    # methods
    # setStartingTiles(self)
    # set the starting state of the sudoko board based on selected starting state (A,B,C), see project documentation
    # for specification of the starting states
    def setStartingTiles(self):
        for row in range(9):
            column = 0
            for tile in self.getRow(row + 1):
                block = self.determineBlockID(row + 1, column + 1)
                if self.startingState[row][column] != '-':
                    tile.setValue(self.startingState[row][column])
                    # we can leverage our forward checking algorithm here in order to easily update all domains to start
                    # values
                    forwardCheck(self, row + 1, column + 1, block, tile.getValue())
                    # then set value of that tiles domain to []
                else:
                    tile.setValue('-')
                column += 1
        return

    # printBoard(self)
    # prints the current state of the board to standard out
    def printBoard(self):
        print("-" * 25)
        # we want to separate the inputs into blocks, which are 3 by 3, keep track and print space for 3
        j = 2
        for row in range(9):
            print("|", end=" ")
            # we want to separate the inputs into blocks, which are 3 by 3, keep track and print space for 3
            i = 2
            for tile in self.getRow(row + 1):
                print(f"{tile.getValue()}", end=' ')
                if i % 3 == 1:
                    print('|', end=" ")
                i += 1
            if j % 3 == 1:
                print()
                print("-" * 25)
            else:
                print()
            j += 1
        return

    # determineBlockID
    # returns the block ID based of Tile position
    # used for initializing tiles, knowing the block number is needed for forward checking and backtracking
    def determineBlockID(self, x, y):
        if x <= 3:
            if y <= 3:
                return 1
            elif y <= 6:
                return 2
            else:
                return 3
        elif x <= 6:
            if y <= 3:
                return 4
            elif y <= 6:
                return 5
            else:
                return 6
        else:
            if y <= 3:
                return 7
            elif y <= 6:
                return 8
            else:
                return 9

    # getRow
    # get all tiles in the specified row
    def getRow(self, row):
        return [tile for tile in self.board if tile.x == row]

    # getColumn
    # get all tiles in the specified column
    def getColumn(self, column):
        return [tile for tile in self.board if tile.y == column]

    # getBlock
    # get all tiles in the specified block
    def getBlock(self, block):
        return [tile for tile in self.board if tile.block == block]

    # isBoardFull
    # checks if the board is filled
    # returns 0 if the board is not full
    # returns 1 if the board is full
    def isBoardFull(self):
        # go through every tile on board
        for tile in self.board:
            # if any tile is not assigned a number return board as not full (0)
            if tile.getValue() == '-':
                return 0
        return 1

    # getTile
    # get a specfic tile based on positional coordinates from the board
    def getTile(self, position):
        # go through every tile and if position given matches that tile
        # then that is the tile to assign, return this tile
        tile = [tile for tile in self.board if tile.x == position[0] and tile.y == position[1]]
        return tile[0]

    # assignTile
    # assigns tile at given position with provided value
    def assignTile(self, position, value):
        # get tile
        tile = self.getTile(position)
        # assign given value to that tile
        tile.setValue(value)


# Tile
# each space in the board is a tile
class Tile:
    # constructor
    def __init__(self, x, y, block, value):
        # instance variables
        self.x = x
        self.y = y
        self.block = block
        self.value = value
        self.domain = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    # methods
    # setValue
    # set the value of the tile to the provided integer value
    def setValue(self, value):
        # check value is within the domain
        # set the value
        self.value = value
        return

    # getValue
    # returns the value of tile
    def getValue(self):
        return self.value

    # getPosition
    # returns the coordinate value of the tile
    def getPosition(self):
        return [self.x, self.y]

    # getDomain
    # returns all values in the domain
    def getDomain(self):
        return self.domain

    # checkIfInDomain
    # checks if the requested value is within the tiles domain
    # returns 1 if value is in domain, returns 0 if not in domain
    def checkDomain(self, domainValue):
        if domainValue in self.getDomain():
            # requested value is found in domain
            return 1
        else:
            return 0

    # isDomainEmpty
    # checks if the tile domain is empty,
    # returns 0 if not empty, returns 1  if empty
    def isDomainEmpty(self):
        if not self.getDomain():
            # domain is empty
            return 1
        else:
            return 0

    # removeFromDomain
    # removes value from the tile domain
    def removeFromDomain(self, valueRemove):
        if self.checkDomain(int(valueRemove)):
            domain = self.getDomain()
            domain.remove(int(valueRemove))
        return

    # getBlockValue
    # returns the block ID value
    def getBlockValue(self):
        return self.block


# functions
# forwardCheck
# our forward checking algorithm
# get all tiles that will be affected by tile (all in same row, all in same column, all in same block)
# update all their domains to remove the value that is chosen
# Check if after the value is removed from the domain, if the domain is empty
# if the new domains are empty, return False
# if the domains are not empty then we return true
def forwardCheck(board, row, column, block, value):
    # get all tiles to forward check, put them all into an iterable zip
    for (x, y, b) in zip(board.getRow(row), board.getColumn(column), board.getBlock(block)):
        # update the domains by removing the value from each domain
        # basically, my code is bad, and it will remove values from domains that have already been solve
        # leading to some domains reaching empty, leading to forward checking to fail when it shouldnt,
        # the easiest solution I found was checking to make sure value is zero before using forward checking to
        # remove from domain
        if x.value == '-':
            x.removeFromDomain(value)
        if y.value == '-':
            y.removeFromDomain(value)
        if b.value == '-':
            b.removeFromDomain(value)
        # check if the new domains are empty, if they are, then forward check returns false
        if x.isDomainEmpty() or y.isDomainEmpty() or b.isDomainEmpty():
            return False
    return True


# backtracking
# our backtracking algorithm
# recursive function
#
def backtracking(board, depth):
    # check if board is full, if it is then good job we did it, return the completed board
    if board.isBoardFull():
        return board
    if depth < 4:
        print("" + "*" * 40 + "\nVariable-assignment " + str(depth + 1) + ":")
        board.printBoard()
    # stuff was double printing in the for loops, so to avoid this we need to track and make sure not repeating
    variable_print = 0
    tile = selectTile(board, depth)
    if depth < 4:
        print("tile selected: " + str(tile.getPosition()))
    # check if none was returned, this might happen, not sure if it would or not, if it does there was an error in
    # selectTile(), indicate there was an error and return the current board state
    if tile is None:
        return board
    # now the actual backtracking
    for possible_value in tile.getDomain():
        if depth < 4 and variable_print == 0:
            print("domain of selected tile is: " + str(tile.domain) + "\ncurrent possible value being tested is: "
                  + str(possible_value))
            variable_print = 1
        # create a new board with the lowest possible value
        # assign_a_vlaue returns a copy of the given board with the given value
        # it will run forward checking as it assigns this value, if forward checking determines that a value is bad,
        # then assign_a_value will return us None
        new_board = assign_a_value(board, tile, possible_value)
        if depth < 4 and (variable_print == 0 or variable_print == 1):
            variable_print = 2
            if new_board is not None:
                print("Board state with testing value:")
                new_board.printBoard()
            else:
                print("Foward Checking found ERROR in domain\n    No board will be printed")
        # if new_board is assigned None, then we need to try the next lowest value in possible_values
        # if it is not none, then we will recursively call backtracking on the new_board
        if new_board is not None:
            # recursively call backtracking
            next_board = backtracking(new_board, depth + 1)
            # if we receive none as a board in at any poinit in our backtracking by forward check, then that is a dead
            # path, and we need to choose a different possible value
            # if we never receive a None, then that means we have selected a correct value, so we return this board
            # it will recursively pass down a completed board to main. And we will receive a solved board
            if next_board is not None:
                if depth < 4:
                    if depth == 3:
                        print("*" * 40 + "\nRecursion is over, the first 4 variables assigned\n" + "*" * 40)
                    print("Variable-assignment " + str(depth + 1) + "\n    Value assigned to selected tile " + str(
                        tile.getPosition()) + " is: " + str(possible_value))
                    print("Board state assigned value:")
                    new_board.printBoard()
                return next_board
    return None


# assign_a_value
# assigns a value to tile and returns a possible board state with that value to backtracking
# possible board state, is a copy of the input board
# after assigning the value, it will preform forward checking to see if any domain gets fucked up
# if forward checking determines that board state isn't possible, then this returns none,
# and the rest is handled by backtracking
def assign_a_value(board, tile, value):
    # create a deepcopy of the board to a new board
    new_board = copy.deepcopy(board)
    tile_position = tile.getPosition()
    # assign the tile selected the chosen value in the new board
    new_board.assignTile(tile_position, value)
    # forward check to make sure such an assignment doesn't fuck everything, if it does then return None to indicate that
    # if it is a bad value then backtracking will handle this and cascade it back (basically move forward and chose a
    # different value to assign this tile)
    # if forward check returns true, then value is okay to choose
    if forwardCheck(new_board, tile_position[0], tile_position[1], tile.getBlockValue(), value):
        return new_board
    # if forward check didn't return true then we return None
    return None


# selectTile
# selects the tile to be used next for backtracking
# selection is based on MRV and the degree heuristic
# ties are broken by left to right, and the up and down
# depth is used for printing first four variable only
def selectTile(board, depth):
    # get list of tiles that have not yet been assigned a value
    tiles_unassigned = [tile for tile in board.board if tile.value == '-']
    # Determine tiles with MRV
    # our MRV is just the domain of the tile
    tiles_MRV = None
    for tile in tiles_unassigned:
        # check domain length of each tile, if it is less than the current tile(s) in tile_MRV, replace tile_MRV
        # with that tile. tiles_MRV is iniated as none so that we no too always add first tile too it
        if tiles_MRV is None or len(tile.getDomain()) < len(tiles_MRV[0].getDomain()):
            tiles_MRV = [tile]
        # if there is a tie in domain length then we append the tile to tiles_MRV to get a list of all tiles
        elif len(tile.getDomain()) == len(tiles_MRV[0].getDomain()):
            tiles_MRV.append(tile)
    # this is used for printing the first 4 variables mrv value only
    if depth < 4:
        print("MRV(domain size) of selected tile: " + str(len(tiles_MRV[0].domain)))
    # for each value in tiles_MRV, we want the degree
    tiles_degree_MRV = None
    # this is used for printing the first 4 variables degree chosen value only
    best_degree_value = 0
    for tile in tiles_MRV:
        # get degree for the tile and if there is a tile already placed in tiles_degree_MRV
        tile_degree = tileDegree(board, tile)
        # if tiles_degree_MRV isn't None(not empty) then we calculate its tile degree
        if tiles_degree_MRV is not None:
            current_tiles_degree_MRV_degree = tileDegree(board, tiles_degree_MRV[0])
        else:
            # if is there none in tiles_degree_MRV set degree value to 10000 to indicate it for comparison
            current_tiles_degree_MRV_degree = 10000
        # compare the value of degree, if there is currently nothing in tiles_degree_MRV add tile to it
        # if degree of tile is less than the degree calculate for the tile in tiles_degree_MRV then replace
        # tiles_degree_MRV with tile
        if tiles_degree_MRV is None or tile_degree < current_tiles_degree_MRV_degree:
            tiles_degree_MRV = [tile]
            best_degree_value = tile_degree
            # if the tile_degree and degree of tiles already in tiles_degree_MRV are equal, append tile to the list
        elif tile_degree == current_tiles_degree_MRV_degree:
            tiles_degree_MRV.append(tile)
    # this is used for printing the first 4 variables mrv value only
    if depth < 4:
        print("Degree of selected tile: " + str(best_degree_value))
    # If there is more than one tile in tiles_degree_MRV
    # break tie by left to right
    if len(tiles_degree_MRV) > 1:
        leftmost_tile = None
        # same as the previous two comparisons, just using the x value of the tile instead of degree or domain length
        for tile in tiles_degree_MRV:
            if leftmost_tile is None or tile.x < leftmost_tile[0].x:
                leftmost_tile = [tile]
            elif tile.x == leftmost_tile[0].x:
                leftmost_tile.append(tile)
        # if there is still more than one tile
        # break tie by up and down
        # not be possible for there be more than 1 tile after this
        if len(leftmost_tile) > 1:
            uppermost_tile = None
            for tile in tiles_degree_MRV:
                if uppermost_tile is None or tile.x < uppermost_tile.x:
                    uppermost_tile = tile
            tile_choice = uppermost_tile
        # else there is a single value in leftmost_tile, we select it as our tile choice
        else:
            tile_choice = leftmost_tile[0]
    # else there is a single tile in tiles_degree_MRV, so we select that tile
    else:
        tile_choice = tiles_degree_MRV[0]
    # return the selected tile to backtracking
    return tile_choice


# tileDegree
# used in tile selection for backtracking
# determines the value of degrees for the selected tile
# degree is the number of empty spaces in the same block, row and column, as the tile
def tileDegree(board, tile):
    # variable to track number of degrees
    degree_count = 0
    # check block
    # get all that are in the same block
    block = board.getBlock(tile.getBlockValue())
    for tile_block in block:
        # make sure to not add the tile as a degree
        if tile_block is not tile and tile_block.getValue() == '-':
            # don't add if in same row and column, otherwise will be added twice by the next to checks (row, and column)
            if tile_block.x != tile.x and tile_block.y != tile.y:
                degree_count += 1
    # check row
    row = board.getRow(tile.x)
    for tile_row in row:
        # make sure to not add the tile as a degree
        if tile_row is not tile and tile_row.getValue() == '-':
            degree_count += 1
    # check column
    column = board.getColumn(tile.y)
    for tile_column in column:
        # make sure to not add the tile as a degree
        if tile_column is not tile and tile_column.getValue() == '-':
            degree_count += 1
    # return degree count
    return degree_count


# printStartingBoardOption
# prints the starting states of the board state, used for menu system
def printStartingBoardOption(boardstate, statetitle):
    print("Starting Board Option " + str(statetitle) + ":")
    j = 2
    print("-" * 24)
    for row in boardstate:
        print("|", end=" ")
        i = 2
        for space in row:
            print(space, end=" ")
            if i % 3 == 1:
                print("|", end=" ")
            i += 1
        print("")
        if j % 3 == 1:
            print("-" * 24)
        j += 1
    return


# main
def main():
    print(
        "\n\n" + "=" * 70 + "\nCS4750 HW6 Group 30\nMembers:\n    Zac Lipperd\n    Carson Rottinghaus\n Description:\n  "
                            "  Implement forward checking ""together with the backtracking\n    search algorithm with "
                            "the MRV and degree heuristics for variable ""\n    selection to solve 9x9 Sudoku "
                            "puzzle\n" + "=" * 70 + "\n\n**Select one of the following sudoko board ""instances**\n")

    # set up starting states
    startA = ["--1--2---", "--5--6-3-", "46---5---", "---1-4---", "6--8--143", "----9-5-8", "8---49-5-", "1--32----",
              "--9---3--"]
    startB = ["--5-1----", "--2--4-3-", "1-9---2-6", "2---3----", "-4----7--", "5----7--1", "---6-3---", "-6-1-----",
              "----7--5-"]
    startC = ["67-------", "-25------", "-9-56-2--", "3---8-9--", "------8-1", "---47----", "--86---9-", "-------1-",
              "1-6-5--7-"]
    # print options to easy see
    printStartingBoardOption(startA, 'A')
    printStartingBoardOption(startB, 'B')
    printStartingBoardOption(startC, 'C')
    print("\n\n" + "=" * 40 + "\n\n")
    while True:
        print("Select board you want from above (A,B or C)")
        print("(or enter X to exit the program)")
        selection = input("enter a letter: ")
        if selection == 'A' or selection == 'a':
            choice = startA
        elif selection == 'B' or selection == 'b':
            choice = startB
        elif selection == 'C' or selection == 'c':
            choice = startC
        elif selection == 'X' or selection == 'x':
            choice = 1000
        else:
            print("Error: Try again (Choose A,B, or C)\n\n")
            choice = -1000
        if choice == -1000:
            pass
        elif choice == 1000:
            break
        else:
            print("\n\n\n*******************************************\nYou have selected starting instance " + selection
                  + "\n*******************************************\nThe first four iterations of back checking will "
                    "be printed\nas "
                    "well as the board state after the variable is "
                    "assigned\n*******************************************\n*Starting Board State*")
            board = Board(choice)
            board.printBoard()
            start = time.time()
            board = backtracking(board, 0)
            end = time.time()
            print("*******************************************\nSolved Board State for instance: " + selection)
            board.printBoard()
            total_time = end - start
            print("Total Execution time of: " + str(total_time) + "\n\n")


if __name__ == "__main__":
    main()
