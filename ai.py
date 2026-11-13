import copy

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


    def find_best_move(self, board, player):
        """
        Find the best move using Alpha-Beta pruning algorithm.
        """
        best_score = float('-inf')
        best_move = None
        alpha = float('-inf')
        beta = float('inf')

        valid_moves = board.get_valid_moves(player)
        if not valid_moves:
            return None

        for move in valid_moves:
            temp_board = copy.deepcopy(board)
            temp_board.execute_move(move[0], move[1], player)

            opponent = 'W' if player == 'B' else 'B'
            score = self.alpha_beta(temp_board, self.depth - 1, alpha, beta, False, player, opponent)

            if score > best_score:
                best_score = score
                best_move = move

            alpha = max(alpha, best_score)

        return best_move

    def alpha_beta_pruning(self, board, depth, alpha, beta, maximizing_player, ai_player, current_turn):
        """
        Recursive minimax algorithm with alpha-beta pruning.
        """
        if depth == 0 or board.is_game_over():
            return self.evaluate(board, ai_player)

        valid_moves = board.get_valid_moves(current_turn)

        if not valid_moves:
            next_turn = 'W' if current_turn == 'B' else 'B'
            return self.alpha_beta_pruning(board, depth - 1, alpha, beta, not maximizing_player, ai_player, next_turn)

        opponent = 'W' if current_turn == 'B' else 'B'

        if maximizing_player:
            max_eval = float('-inf')
            for move in valid_moves:
                temp_board = copy.deepcopy(board)
                temp_board.execute_move(move[0], move[1], current_turn)

                eval = self.alpha_beta_pruning(temp_board, depth - 1, alpha, beta, False, ai_player, opponent)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval

        else:
            min_eval = float('inf')
            for move in valid_moves:
                temp_board = copy.deepcopy(board)
                temp_board.execute_move(move[0], move[1], current_turn)

                eval = self.alpha_beta_pruning(temp_board, depth - 1, alpha, beta, True, ai_player, opponent)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval