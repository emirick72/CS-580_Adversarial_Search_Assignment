class Board:
    """
    Board class that manages board rules and logic.
    """
    def __init__(self, size=8):
        """
        Initialize the game's board and the black and white player pieces.
        """
        self.size = size
        self.board = [['.' for _ in range(size) for _ in range(size)]]

        # Set up initial game pieces
        mid = size // 2
        self.board[mid - 1][mid - 1] = 'W'
        self.board[mid][mid] = 'W'
        self.board[mid - 1][mid] = 'B'
        self.board[mid][mid - 1] = 'B'

    def display(self):
        """
        Display the board with coordinates for players to use.
        """
        print("  " + " ".join([str(i) for i in range(self.size)]))
        for r in range(self.size):
            print(f"{r} " + " ".join(self.board[r]))
        print()

    def is_on_board(self, row, col):
        """
        Check if pieces are on the board before playing.
        """
        return 0 <= row < self.size and 0 <= col < self.size

    def get_valid_moves(self, player):
        """
        Get and return a list of valid player moves.
        All valid moves are represented by a list of (row, col) tuples.
        """
        valid_moves = []
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] == '.' and self.is_valid_move(r, c, player):
                    valid_moves.append((r, c))
        return valid_moves

    def is_valid_move(self, row, col, player):
        """
        Check if a move is valid or not.
        """
        if self.board[row][col] != '.':
            return False

        opponent = 'W' if player == 'B' else 'B'
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dr, dc in directions:
            r, c = row + dr, col + dc
            found_opponent = False
            while self.is_on_board(r, c) and self.board[r][c] == opponent:
                r += dr
                c += dc
                found_opponent = True
            if found_opponent and self.is_on_board(r, c) and self.board[r][c] == player:
                return True

        return False

    def execute_move(self, row, col, player):
        """
        Place the disks and flip the opponent's disks.
        """
        self.board[row][col] = player
        opponent = 'W' if player == 'B' else 'B'
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dr, dc in directions:
            r, c = row + dr, col + dc
            to_flip = []

            while self.is_on_board(r, c) and self.board[r][c] == opponent:
                to_flip.append((r, c))
                r += dr
                c += dc

            if to_flip and self.is_on_board(r, c) and self.board[r][c] == player:
                for fr, fc in to_flip:
                    self.board[fr][fc] = player

    def get_score(self):
        """
        Return the count of both black and white disks per player.
        """
        black_count = sum(row.count('B') for row in self.board)
        white_count = sum(row.count('W') for row in self.board)
        return black_count, white_count

    def is_game_over(self):
        """
        Check if the game is over or not, based on if either player has any valid moves left.
        """
        return not self.get_valid_moves('B') and not self.get_valid_moves('W')