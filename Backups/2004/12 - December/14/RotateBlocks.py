def rotateLeft(piece):
    newPiece = [0, 0, 0,
                0, 0, 0,
                0, 0, 0]

    newPiece[0] = piece[2]  # The corners
    newPiece[2] = piece[8]
    newPiece[8] = piece[6]
    newPiece[6] = piece[0]
    
    newPiece[1] = piece[5]  # N, E, S, W
    newPiece[5] = piece[7]
    newPiece[7] = piece[3]
    newPiece[3] = piece[1]

    return newPiece

def rotateRight(piece):
    newPiece = [0, 0, 0,
                0, 0, 0,
                0, 0, 0]

    newPiece[0] = piece[2]  # The corners
    newPiece[8] = piece[2]
    newPiece[6] = piece[8]
    newPiece[0] = piece[6]
    
    newPiece[5] = piece[1]  # N, E, S, W
    newPiece[7] = piece[5]
    newPiece[3] = piece[7]
    newPiece[1] = piece[3]

    return newPiece