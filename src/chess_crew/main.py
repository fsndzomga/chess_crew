#!/usr/bin/env python
from chess_crew.crew import ChessCrew
import chess
import chess.engine

def run():

    # Initialize a chess board and the chess engine
    engine = chess.engine.SimpleEngine.popen_uci("/opt/homebrew/Cellar/stockfish/16/bin/stockfish")

    # Configure Stockfish to a specific skill level, e.g., 10
    engine.configure({"Skill Level": 0})

    # pdb.set_trace()

    def play_game():
        moves = []  # Variable to store the list of moves
        board = chess.Board()

        def get_agent_move(board):
            feedback = ""
            while True:

                # Replace with your inputs, it will automatically interpolate any tasks and agents information
                inputs = {
                    'board': board,
                    'moves': moves,
                    'legal_moves': list(board.legal_moves),
                    'feedback': feedback,
                }

                result = ChessCrew().crew().kickoff(inputs=inputs)

                next_move = result

                try:
                    move = chess.Move.from_uci(next_move)

                    if move in board.legal_moves:
                        return move
                    else:
                        feedback = f"Agent's generated move {move} is not valid currently."
                except:
                    feedback = "Failed to parse the Agent's generated move. Retrying..."

        while not board.is_game_over():
            if board.turn:  # True for white's turn, False for black's turn
                result = engine.play(board, chess.engine.Limit(time=0.001))
                board.push(result.move)
                moves.append(result.move.uci())  # Store UCI move in the list
            else:
                move = get_agent_move(board)
                board.push(move)
                moves.append(move.uci())  # Store UCI move in the list
            print(board)
            print("\n\n")

        # Check the result of the game
        winner = ""
        if board.is_checkmate():
            if board.turn:
                winner = "Black"
            else:
                winner = "White"
        elif board.is_stalemate() or board.is_insufficient_material() or board.is_seventyfive_moves() or board.is_fivefold_repetition() or board.is_variant_draw():
            winner = "Draw"

        if winner == "Black":
            return "Agent wins by checkmate."
        elif winner == "White":
            return "Stockfish wins by checkmate."
        else:
            return "The game is a draw."

    # Number of games to play
    n_games = 1

    # Initialize a dictionary to store the results
    results = {"Agent wins": 0, "Stockfish wins": 0, "Draw": 0}

    # Run the game n times
    for i in range(n_games):
        # print(f"Starting game {i+1}...")
        result = play_game()
        print(result)

        # Update the results dictionary based on the outcome of the game
        if "Agent wins" in result:
            results["Agent wins"] += 1
        elif "Stockfish wins" in result:
            results["Stockfish wins"] += 1
        else:
            results["Draw"] += 1

        # print(f"Game {i+1} finished.\n\n")

    # Print the final results
    print("Final results after playing", n_games, "games:")
    print("Agent won:", results["Agent wins"], "games")
    print("Stockfish won:", results["Stockfish wins"], "games")
    print("Draw:", results["Draw"], "games")
