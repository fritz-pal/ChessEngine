import chess

from Engine import set_position, get_best_move, reset_board

def receive_command(command, params):
    match command:
        case "uci":
            uci()
        case "quit":
            return True
        case "position":
            position_cmd(params)
        case "isready":
            is_ready()
        case "go":
            go()
        case "help":
            help()
        case "ucinewgame":
            reset_board()
        case "option":
            return False
        case _:
            print(f'Unknown command: "{command}". Type help for more information.')
    return False

def position_cmd(params):
    set_position(params)

def go():
    print("bestmove " + get_best_move())

def help():
    print("Enginepal is normally used with a graphical user interface (GUI) and implements the Universal Chess Interface (UCI) protocol to communicate with a GUI, an API, etc.")

def is_ready():
    print("readyok")

def uci():
    print("id name Enginepal\nid author Fritzpal\nuciok")

def run_uci():
    while True:
        line = input().strip()
        split = line.split()
        command = split[0] if split else None
        params = split[1:] if len(split) > 1 else []
        if receive_command(command, params):
            break