import random

# The various pieces in the game

def getPiece():
    pieceCount = len(piecesArray)
    pieceNum = random.randomInt(0, pieceCount - 1)
    return piecesArray[pieceNum]

piecesArray = [[0, 0, 0,
                1, 1, 1,
                0, 0, 0],

               [1, 1, 1,
                1, 0, 0,
                1, 1, 1],

               [1, 0, 1,
                1, 1, 1,
                1, 0, 1],

               [1, 1, 0,
                1, 1, 1,
                0, 0, 0],

               [1, 1, 0,
                1, 1, 1,
                0, 1, 0],

               [1, 1, 0,
                1, 1, 0,
                0, 1, 0],

               [0, 1, 0,
                1, 1, 1,
                0, 0, 0],

               [1, 1, 0,
                0, 1, 1,
                1, 1, 0],

               [0, 1, 1,
                0, 1, 0,
                1, 1, 0],

               [1, 1, 0,
                0, 1, 0,
                0, 1, 1],

               [0, 1, 0,
                1, 1, 1,
                0, 1, 0],

               [0, 0, 0,
                1, 1, 1,
                1, 0, 0],

               [1, 1, 0,
                1, 0, 0,
                1, 1, 0],

               [0, 0, 0,
                1, 1, 1,
                0, 0, 1],

               [0, 0, 0,
                0, 1, 1,
                0, 1, 0],

               [1, 1, 0,
                1, 1, 1,
                1, 1, 0],

               [1, 1, 1,
                1, 1, 0,
                1, 1, 0],

               [1, 1, 1,
                1, 0, 1,
                1, 0, 0],

               [1, 1, 1,
                1, 0, 1,
                0, 0, 1],

               [1, 1, 1,
                1, 0, 0,
                1, 0, 0],

               [1, 1, 0,
                1, 1, 0,
                1, 1, 1],

               [1, 1, 0,
                1, 1, 0,
                1, 1, 0],
          
               [1, 1, 0,
                1, 1, 0,
                0, 0, 0]]