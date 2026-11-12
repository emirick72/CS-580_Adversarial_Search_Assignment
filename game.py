from board import Board

class OthelloGame:
    def __init__(self, size=8):
        """
        Initialize the game board.
        """
        self.board = Board(size)
        self.current_player = 'B'

    def play(self):
        """
        Function to start the game.
        """
        print("--- Welcome to Othello (Reversi)! ---")
        print("Black = B\nWhite = W\n")

        while not self.board.is_game_over():
            self.board.display()
            valid_moves = self.board.get_valid_moves(self.current_player)

            print(f"Current Player: {'Black (B)' if self.current_player == 'B' else 'White (W)'}")

            if not valid_moves:
                print(f"No valid moves available for {self.current_player}. Your turn is skipped.\n")
                self.current_player = 'W' if self.current_player == 'B' else 'B'
                continue

            print(f"Valid moves: {valid_moves}")

            try:
                move_input = input("Enter move as 'row col' (e.g., 2 3): ")
                r, c = map(int, move_input.strip().split())

                if (r, c) in valid_moves:
                    self.board.execute_move(r, c, self.current_player)
                    self.current_player = 'W' if self.current_player == 'B' else 'B'
                else:
                    print("Invalid move. Try again.\n")
            except (ValueError, IndexError):
                print("Invalid input format. PLease enter row and column separated by a space.\n")


        self.board.display()
        print("--- Game Over ---")
        black_score, white_score = self.board.get_score()
        print(f"Final Score:\n")
        print(f"Black (B): {black_score} | White (W): {white_score}")

        if black_score > white_score:
            print("Black wins!")
        elif white_score > black_score:
            print("White wins!")
        else:
            print("Tie game!")