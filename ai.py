class OthelloAIPlayer:
    def __init__(self, depth=4):
        self.depth = depth

    # Positional weight matrix for the game
    WEIGHTS_8X8 = [
        [120, -20, 20, 5, 5, 20, -20, 120],
        [-20, -40, -5, -5, -5, -5, -40, -20],
        [20, -5, 15, 3, 3, 15, -5, 20],
        [5, -5, 3, 3, 3, 3, -5, 5],
        [5, -5, 3, 3, 3, 3, -5, 5],
        [20, -5, 15, 3, 3, 15, -5, 20],
        [-20, -40, -5, -5, -5, -5, -40, -20],
        [120, -20, 20, 5, 5, 20, -20, 120]
    ]

    def evaluate(self, board, player):
        """
        Heuristic evaluation function for intermediate states.
        """
        opponent = 'W' if player == 'B' else 'B'

        pos_score = 0
        size = board.size
        for r in range(size):
            for c in range(size):
                if board.board[r][c] == player:
                    if size == 8:
                        pos_score += self.WEIGHTS_8X8[r][c]
                    else:
                        if (r == 0 or r == size - 1) and (c == 0 or c == size - 1):
                            pos_score += 20
                        else:
                            pos_score += 1

                elif board.board[r][c] == opponent:
                    if size == 8:
                        pos_score -= self.WEIGHTS_8X8[r][c]
                    else:
                        if (r == 0 or r == size - 1) and (c == 0 or c == size - 1):
                            pos_score -= 20
                        else:
                            pos_score -= 1

        player_moves = len(board.get_valid_moves(player))
        opponent_moves = len(board.get_valid_moves(opponent))
        mobility_score = player_moves - opponent_moves

        b_count, w_count = board.get_score()
        piece_score = (b_count - w_count) if player == 'B' else (w_count - b_count)

        total_score = (10 * pos_score) + (5 * mobility_score) + (1 * piece_score)
        return total_score