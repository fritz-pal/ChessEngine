import csv
import random
import chess
import sys, os

openings = {}

def convert_to_uci(moves):
    uci_moves = []
    board = chess.Board()
    for move in moves:
        parsed_move = board.parse_san(move)
        uci_moves.append(parsed_move.uci())
        board.push(parsed_move)
    return uci_moves

def load_openings(): 
    try:
        path = sys._MEIPASS
    except:
        path = os.path.abspath('.')
    global openings
    openings = {}
    with open(os.path.join(path, 'chess_openings.csv'), mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            moves = []
            for move in row['moves'].strip().split(" "):
                if "." in move:
                    moves.append(move.split(".")[1])
                else:
                    moves.append(move)
            openings[row['name']] = convert_to_uci(moves)
            
def get_opening_move(board : chess.Board):
    global openings
    algebraic_move = None
    if board.ply() == 0:
        opening = random.choice(list(openings.values()))
        algebraic_move = opening[0]
    else:
        possible_openings = []
        move_stack = board.move_stack
        for key in openings.keys():
            opening = openings[key]
            if len(opening) <= len(move_stack):
                continue
            possible = True
            for i in range(len(move_stack)):
                if opening[i] != move_stack[i].uci():
                    possible = False
                    break
            if possible:
                possible_openings.append(key)
        if len(possible_openings) == 0:
            return None
        opening = random.choice(possible_openings)
        algebraic_move = openings[opening][len(move_stack)]   
        print("found opening move from opening", opening)      
    return board.parse_san(algebraic_move)