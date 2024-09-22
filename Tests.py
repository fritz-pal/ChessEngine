from Engine import position, get_best_move, count_material, distance, endgame_evaluation, is_opening
from Openings import get_opening_move, load_openings
import chess

def test_distance():
    print(distance(chess.C4, chess.C5)) # 1
    print(distance(chess.A1, chess.H1)) # 7
    print(distance(chess.A2, chess.B7)) # 5

def test_endgame_evaluation():
    position.set_fen("3r4/4k3/8/8/4K3/8/8/8 w - - 0 1")
    print(endgame_evaluation(position, position.turn))
#test_endgame_evaluation()

def test_positions():
    global is_opening
    is_opening = False
    print("material:", count_material(position, True))
    position.set_fen("8/2k5/P7/8/5n1P/1N3P2/2p1KP2/3rB3 w - - 7 50")
    print("best move:", get_best_move(), "material:", count_material(position, not position.turn))
    position.set_fen("rnbk1bnr/ppNp1pp1/6qp/8/3pPB2/8/PPPN1PPP/R2QKB1R b KQ - 2 8")
    print("best move:", get_best_move(), "material:", count_material(position, not position.turn))
    position.set_fen("1k1r4/ppp2pp1/5n1p/1PP2q2/1Q6/5N1P/3N1PP1/4R1K1 b - - 0 27")
    print("best move:", get_best_move(), "material:", count_material(position, not position.turn))
    position.set_fen("7k/p5pp/8/5r2/2p5/2PR4/PP1B2PP/6K1 w - - 0 37")
    print("best move:", get_best_move(), "material:", count_material(position, not position.turn))
    position.set_fen("8/5ppn/4k2p/8/K7/5P1P/2r5/1q6 b - - 2 49")
    print("best move:", get_best_move(), "material:", count_material(position, not position.turn))
test_positions()

def test_openings():
    load_openings()
    test_board = chess.Board()
    move = get_opening_move(test_board)
    print(move)
    test_board.push(move)
    move = get_opening_move(test_board)
    print(move)
    test_board.push(move)
    move = get_opening_move(test_board)
    print(move)
    test_board.push(move)
    move = get_opening_move(test_board)
    print(move)
    test_board.push(move)
    move = get_opening_move(test_board)
    print(move)
    test_board.push(move)
    move = get_opening_move(test_board)
    print(move)
    test_board.push(move)
#test_openings()
