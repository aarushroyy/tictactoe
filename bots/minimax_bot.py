import random
from .bot_interface import BotInterface

class MinimaxBot(BotInterface):
    def __init__(self, difficulty='medium'):
        super().__init__(difficulty)
        
        difficulty = difficulty.lower()
        # self.random_move_chance = {
        #     'easy': 0.7,
        #     'medium': 0.3,
        #     'hard': 0.0 
        # }[difficulty]

    def get_move(self, board):
        """Get the next move based on difficulty level"""
        if self.difficulty == 'easy':
            return self._get_random_move(board)
        elif self.difficulty == 'medium':
            if random.random() < 0.5:
                return self._get_random_move(board)
            else:
                return self._get_minimax_move(board)
        else:  
            return self._get_minimax_move(board)

    def _get_random_move(self, board):
        """Make a completely random move from available positions"""
        empty_cells = [(i, j) for i in range(3) for j in range(3) if board[i][j] is None]
        return random.choice(empty_cells) if empty_cells else None
    
    def _get_minimax_move(self, board):
        """Get the best move using minimax algorithm"""
        best_val = float('-inf')
        best_move = None

        for i in range(3):
            for j in range(3):
                if board[i][j] is None:
                    # tries the move
                    board[i][j] = 0  # 0 represents O (bot)
                    move_val = self._minimax(board, 0, False)
                    # for undo
                    board[i][j] = None

                    if move_val > best_val:
                        best_move = (i, j)
                        best_val = move_val

        return best_move

    def _minimax(self, board, depth, is_maximizing):
        """Minimax algorithm implementation"""
        score = self._evaluate(board)
        
        # If we have a winner or draw
        if score is not None:
            return score

        if is_maximizing:
            best = float('-inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] is None:
                        board[i][j] = 0  # O's move
                        best = max(best, self._minimax(board, depth + 1, False))
                        board[i][j] = None
            return best
        else:
            best = float('inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] is None:
                        board[i][j] = 1  # X's move
                        best = min(best, self._minimax(board, depth + 1, True))
                        board[i][j] = None
            return best

    def _evaluate(self, board):
        """Evaluate the current board state"""
        # Check rows
        for row in range(3):
            if board[row][0] == board[row][1] == board[row][2] is not None:
                return 10 if board[row][0] == 0 else -10

        # Check columns
        for col in range(3):
            if board[0][col] == board[1][col] == board[2][col] is not None:
                return 10 if board[0][col] == 0 else -10

        # Check diagonals
        if board[0][0] == board[1][1] == board[2][2] is not None:
            return 10 if board[0][0] == 0 else -10
        if board[0][2] == board[1][1] == board[2][0] is not None:
            return 10 if board[0][2] == 0 else -10

        # Check for draw or ongoing game
        has_empty = False
        for i in range(3):
            for j in range(3):
                if board[i][j] is None:
                    has_empty = True
                    break
            if has_empty:
                break

        return 0 if not has_empty else None