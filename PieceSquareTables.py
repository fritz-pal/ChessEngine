import chess

PAWN_VALUE = 100
KNIGHT_VALUE = 300
BISHOP_VALUE = 310
ROOK_VALUE = 500
QUEEN_VALUE = 900
KING_VALUE = 0

ROOK_TABLE = [
    0,  0,  0,  0,  0,  0,  0,  0,
    10, 20, 20, 20, 20, 20, 20, 10,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5, -5,  5, 10, 10,  5, -5, -5
]

KNIGHT_TABLE = [
    -50,-40,-30,-30,-30,-30,-40,-50,
    -40,-20,  0,  0,  0,  0,-20,-40,
    -30,  0, 10, 15, 15, 10,  0,-30,
    -30,  5, 15, 20, 20, 15,  5,-30,
    -30,  0, 15, 20, 20, 15,  0,-30,
    -30,  5, 10, 15, 15, 10,  5,-30,
    -40,-20,  0,  5,  5,  0,-20,-40,
    -50,-40,-30,-30,-30,-30,-40,-50,
]

BISHOP_TABLE = [
    -20,-10,-10,-10,-10,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5, 10, 10,  5,  0,-10,
    -10,  5,  5, 10, 10,  5,  5,-10,
    -10,  0, 10, 10, 10, 10,  0,-10,
    -10, 10, 10, 0, 0, 10, 10,  -10,
    -10, 20,  0,  5,  5,  0, 20,-10,
    -20,-10,-30,-10,-10,-30,-10,-20,
]

QUEEN_TABLE = [
    -20,-10,-10, -5, -5,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5,  5,  5,  5,  0,-10,
    -5,  0,  5,  5,  5,  5,  0, -5,
    -5,  0,  5,  5,  5,  5,  0, -5,
    -10,  5,  5,  5,  5,  5,  0,-10,
    -10,  0,  5,  5,  5,  0,  0,-10,
    -20,-10,-10, -5, -5,-10,-10,-20
]

KING_TABLE = [
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -20,-30,-30,-40,-40,-30,-30,-20,
    -10,-20,-20,-20,-20,-20,-20,-10,
    20, 20,  0,  0,  0,  0, 20, 20,
    20, 30, 10, -20, 0, -10, 30, 20
]

KING_TABLE_ENDGAME = [
    -10, -5, -5, -5, -5, -5, -5, -10,
    -5, 0, 0,  0,  0,  0,  0, -5,  
    -5, 0, 10, 10, 10,  10,  0, -5,
    -5, 0, 10, 10, 10,  10,  0, -5,
    -5, 0, 10, 10, 10,  10,  0, -5,
    -5, 0, 10, 10, 10,  10,  0, -5,
    -5, 0,  0,  0,  0,  0,  0, -5,
    -10, -5, -5, -5, -5, -5, -5, -10
]

PAWN_TABLE = [
    0,  0,  0,  0,  0,  0,  0,  0,
    50, 50, 50, 50, 50, 50, 50, 50,
    10, 10, 20, 30, 30, 20, 10, 10,
    5,  5, 10, 25, 25, 10,  5,  5,
    0,  0,  0, 20, 20,  0,  0,  0,
    10, 10, -10, 0, 0, -10, -5, 10,
    5, 10, 10, -20, -20, 10, 10, 5,
    0,  0,  0,  0,  0,  0,  0,  0
]

PAWN_TABLE_ENDGAME = [
    0,  0,  0,  0,  0,  0,  0,  0,
    60, 60, 60, 60, 60, 60, 60, 60,
    30, 30, 30, 30, 30, 30, 30, 30,
    20, 20, 20, 20, 20, 20, 20, 20,
    10, 10, 10, 10, 10, 10, 10, 10,
    -5, -5, -5, -5, -5, -5, -5, -5,
    -10, -10, -10, -10, -10, -10, -10, -10,
    0,  0,  0,  0,  0,  0,  0,  0    
]

FLIP_TABLE = [
    56, 57, 58, 59, 60, 61, 62, 63,
    48, 49, 50, 51, 52, 53, 54, 55,
    40, 41, 42, 43, 44, 45, 46, 47,
    32, 33, 34, 35, 36, 37, 38, 39,
    24, 25, 26, 27, 28, 29, 30, 31,
    16, 17, 18, 19, 20, 21, 22, 23,
    8,  9,  10, 11, 12, 13, 14, 15,
    0,  1,  2,  3,  4,  5,  6,  7
]

def get_static_piece_value(piece):
    match piece:
        case chess.PAWN:
            return PAWN_VALUE
        case chess.KNIGHT:
            return KNIGHT_VALUE
        case chess.BISHOP:
            return BISHOP_VALUE
        case chess.ROOK:
            return ROOK_VALUE
        case chess.QUEEN:
            return QUEEN_VALUE
        case chess.KING:
            return KING_VALUE
        case _:
            return 0

def get_piece_value(square, piece, color, is_endgame):
    match piece:
        case chess.PAWN:
            if is_endgame:
                return PAWN_VALUE + PAWN_TABLE_ENDGAME[square] if not color else PAWN_VALUE + PAWN_TABLE_ENDGAME[FLIP_TABLE[square]]
            return PAWN_VALUE + PAWN_TABLE[square] if not color else PAWN_VALUE + PAWN_TABLE[FLIP_TABLE[square]]
        case chess.KNIGHT:
            return KNIGHT_VALUE + KNIGHT_TABLE[square] if not color else KNIGHT_VALUE + KNIGHT_TABLE[FLIP_TABLE[square]]
        case chess.BISHOP:
            return BISHOP_VALUE + BISHOP_TABLE[square] if not color else BISHOP_VALUE + BISHOP_TABLE[FLIP_TABLE[square]]
        case chess.ROOK:
            return ROOK_VALUE + ROOK_TABLE[square] if not color else ROOK_VALUE + ROOK_TABLE[FLIP_TABLE[square]]
        case chess.QUEEN:
            return QUEEN_VALUE + QUEEN_TABLE[square] if not color else QUEEN_VALUE + QUEEN_TABLE[FLIP_TABLE[square]]
        case chess.KING:
            if is_endgame:
                return KING_VALUE + KING_TABLE_ENDGAME[square] if not color else KING_VALUE + KING_TABLE_ENDGAME[FLIP_TABLE[square]]
            return KING_VALUE + KING_TABLE[square] if not color else KING_VALUE + KING_TABLE[FLIP_TABLE[square]]
        case _:
            return 0