import sys
import random
import chess

PIECE_VALUES = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
}

def get_capture_value(board, move):
    captured_piece = board.piece_at(move.to_square)
    if captured_piece != None:
        return PIECE_VALUES.get(captured_piece.piece_type, 0)
    return 0

def my_moving_strategy(board):
    all_moves = list(board.legal_moves)
    
    if len(all_moves) == 0:
        return None
    
    # Capture method (capture the highest value)
    capture_list = []
    for m in all_moves:
        if board.is_capture(m) == True:
            capture_list.append(m)
    
    if len(capture_list) > 0:
        max_value = 0
        for m in capture_list:
            val = get_capture_value(board, m)
            if val > max_value:
                max_value = val
        
        best_captures = []
        for m in capture_list:
            if get_capture_value(board, m) == max_value:
                best_captures.append(m)
        
        return random.choice(best_captures)
    
    # Else random move
    else:
        return random.choice(all_moves)

def main():
    board = chess.Board()
    force_mode = False
    
    while True:
        try:
            line = sys.stdin.readline()
        except:
            break
        
        if not line:
            break
        
        input_list = line.split()
        if len(input_list) == 0:
            continue
        
        command = input_list[0]
        
        # XBoard interface
        if command == "protover":
            print('feature myname="Fortune_Wheel" usermove=1 done=1')
            sys.stdout.flush()
        
        elif command == "new":
            board = chess.Board()
            force_mode = False
        
        elif command == "quit":
            break
        
        elif command == "force":
            force_mode = True
        
        # My turn
        elif command == "go":
            force_mode = False
            my_move = my_moving_strategy(board)
            if my_move != None:
                board.push(my_move)
                print('move', my_move)
                sys.stdout.flush()
        
        # Opponent's turn
        elif command == "usermove":
            try:
                opponent_move_str = input_list[1]
                move = chess.Move.from_uci(opponent_move_str)
                board.push(move)
                
                if force_mode == False:
                    response = my_moving_strategy(board)
                    if response != None:
                        board.push(response)
                        print('move', response)
                        sys.stdout.flush()
            except:
                pass

if __name__ == "__main__":
    main()