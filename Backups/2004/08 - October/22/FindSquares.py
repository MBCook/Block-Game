from GameBoard import GameBoard

def findSquares(board):
    """Find complete squares of 3x3

    Return None if nothing is found
    Otherwise return a tuple.
        The first element is the number of squares found.
        The second is a copy of the board with each dead square marked."""

    newBoard = GameBoard()

    newBoard.copy(board)

    squareCount = 0

    # All setup, just mark those squares (if they exist)

    for j in range(newBoard.getHeight() - 3):
        for i in range(newBoard.getWidth() - 3):
            if newBoard.squareAt(i, j, 1):
                squareCount = squareCount + 1

    # Marked, check things

    if squareCount > 0:
        return (squareCount, newBoard)
    else:
        return None