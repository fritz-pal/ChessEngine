import chess
import time

from PieceSquareTables import get_piece_value, get_static_piece_value
from Openings import get_opening_move, load_openings

position = chess.Board()
best_move = chess.Move.null()
moves_searched = 0
search_depth = 4
is_endgame = False
is_opening = True
load_openings()

def reset_board():
    global position, is_endgame, is_opening
    position = chess.Board()
    is_endgame = False
    is_opening = True
    
def set_position(params):
    global position, is_opening
    if params[0] == "startpos":
        position = chess.Board()
    elif params[0] == "fen":
        fen = " ".join(params[1:params.index("moves")]) if "moves" in params else " ".join(params[1:])
        position.set_fen(fen)
        is_opening = False
    if "moves" in params:
        for move in params[params.index("moves") + 1:]:
            position.push(chess.Move.from_uci(move))
    
def evaluate(board : chess.Board):
    evaluation = 0
    outcome = board.outcome()
    if outcome:
        if outcome.winner == None:
            return 0
        elif outcome.winner == board.turn:
            return -9999
        else:
            return 9999
    evaluation = count_material(board, chess.WHITE) - count_material(board, chess.BLACK)
    if not board.turn:
        evaluation *= -1
    #if is_endgame:
    #    evaluation += endgame_evaluation(board, board.turn)
    return evaluation

def endgame_evaluation(board : chess.Board, isWhite):
    evaluation = 0
    own_king = board.king(isWhite)
    opponent_king = board.king(not isWhite)
    evaluation += 10 * int(distance(own_king, opponent_king))
    evaluation += 10 * int(14 - distance(chess.D4, opponent_king))
    return evaluation

def distance(square1, square2):
    return abs(square1 / 8 - square2 / 8) + abs(square1 % 8 - square2 % 8)

def count_material(board, color):
    material = 0
    for square, piece in board.piece_map().items():
        if piece.color == color:
            material += get_piece_value(square, piece.piece_type, color, is_endgame)
    return material

def print_info(eval):
    eval_msg = "cp 0"
    if eval > 9900 or eval < -9900:
        if eval > 0:
            eval_msg = "mate " + str(int((search_depth - (10000 - eval)) / 2))
        else:
            eval_msg = "mate " + str(int((search_depth - (10000 + eval)) / 2))
    else:
        eval_msg = "cp " + str(eval)
    print("info score", eval_msg, "depth", search_depth)
    
def get_best_move():
    global best_move, moves_searched, search_depth, is_endgame, is_opening, position
    best_move = chess.Move.null()
    moves_searched = 0
    
    if not is_endgame:
        opponentMaterial = count_material(position, not position.turn)
        if opponentMaterial <= 800:
            is_endgame = True  
    if is_opening:
        move = get_opening_move(position)
        if move:
            print("info score cp 0 depth 0")
            return move.uci()
        else:
            is_opening = False
    ms = time.time()
    eval = search(search_depth, -99999, 99999)
    msg = "searched " + str(moves_searched) + " positions in " + str(int((time.time() - ms) * 1000)) + "ms"
    if best_move == chess.Move.null():
        msg += " result was null -> returning random move"
        print(msg)
        return get_random_move().uci()
    print(msg)
    print_info(eval)
    return best_move.uci()

def get_ordered_moves(only_captures = False):
    if only_captures:
        moves = list(position.generate_legal_captures())
        if len(moves) == 0:
            return moves
        moves.sort(key = lambda move: get_static_piece_value(position.piece_at(move.to_square).piece_type) if position.piece_at(move.to_square) else 1, reverse = True)
        return moves
    
    moves = list(position.legal_moves)
    if len(moves) == 0:
        return moves
    moves.sort(key = lambda move: (position.is_capture(move), get_static_piece_value(position.piece_at(move.to_square).piece_type) if position.piece_at(move.to_square) else 0), reverse = True)
    return moves

def get_random_move():
    moves = get_ordered_moves()
    if len(moves) == 0:
        return chess.Move.null()
    for move in moves:
        position.push(move)
        if position.is_checkmate():
            position.pop()
            return move
        position.pop()
    moves.sort(key = lambda move: (position.gives_check(move), position.is_capture(move)), reverse=True)
    return moves[0]

def search(depth, alpha, beta):
    #print(position)
    #print("depth:", depth, "alpha:", alpha, "beta:", beta)
    if depth == 0:
       return search_only_captures(10, alpha, beta)
       #return evaluate(position)
    
    if position.can_claim_draw():
        return 0
    
    moves = get_ordered_moves()
    #print("moves:", moves)
    if len(moves) == 0:
        if position.is_check():
            return -10000 - depth
        else:
            return 0
    global best_move, moves_searched, search_depth
    for move in moves:
        position.push(move)
        moves_searched += 1
        #print("checking move:", move)
        score = -search(depth - 1, -beta, -alpha)
        position.pop()
        #print("score:", score)
        if score >= beta:
            if depth == search_depth:
                #print("cutoff -> returning", beta, "for move", move)
                best_move = move
            else:
                return beta
        if score > alpha:
            alpha = score
            if depth == search_depth:
                best_move = move
    return alpha

def search_only_captures(sel_depth, alpha, beta):
    global moves_searched
    evaluation = evaluate(position)
    if evaluation >= beta:
        return beta
    alpha = max(alpha, evaluation)
    if sel_depth == 0:
        return alpha
    moves = get_ordered_moves(only_captures = True)
    for move in moves:
        position.push(move)
        moves_searched += 1
        score = -search_only_captures(sel_depth - 1, -beta, -alpha)
        position.pop()
        if score >= beta:
            return beta
        alpha = max(alpha, score)
    return alpha