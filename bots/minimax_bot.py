import random
from .bot_interface import BotInterface

class MinimaxBot(BotInterface):
    # def __init__(self, difficulty='medium'):
    #     super().__init__(difficulty)
        
    #     difficulty = difficulty.lower()
    #     # self.random_move_chance = {
    #     #     'easy': 0.7,
    #     #     'medium': 0.3,
    #     #     'hard': 0.0 
    #     # }[difficulty]

    # def get_move(self, board):
    #     """Get the next move based on difficulty level"""
    #     if self.difficulty == 'easy':
    #         return self._get_random_move(board)
    #     elif self.difficulty == 'medium':
    #         if random.random() < 0.5:
    #             return self._get_random_move(board)
    #         else:
    #             return self._get_minimax_move(board)
    #     else:  
    #         return self._get_minimax_move(board)
    
    def __init__(self, difficulty='medium'):
        super().__init__(difficulty)
        
        # New: Add configuration for each difficulty
        self.config = {
            'easy': {
                'max_depth': 1,      # Shallow search
                'best_move_prob': 0.2 # 20% chance of best move
            },
            'medium': {
                'max_depth': 2,      # Moderate search
                'best_move_prob': 0.6 # 60% chance of best move
            },
            'hard': {
                'max_depth': float('inf'), # Full search
                'best_move_prob': 0.95     # 95% chance of best move
            }
        }[difficulty.lower()]

    def get_move(self, board):
        """Modified: Get move with probability-based selection"""
        # Get all possible moves with their scores
        scored_moves = []
        for i in range(3):
            for j in range(3):
                if board[i][j] is None:
                    board[i][j] = 0  # Try move
                    score = self._minimax(board, 0, False)
                    board[i][j] = None  # Undo move
                    scored_moves.append(((i, j), score))
        
        if not scored_moves:
            return None

        # Sort moves by score
        scored_moves.sort(key=lambda x: x[1], reverse=True)
        best_move = scored_moves[0][0]
        
        # Use probability to choose between best and random moves
        if random.random() < self.config['best_move_prob']:
            return best_move
        else:
            other_moves = [move[0] for move in scored_moves[1:]]
            return random.choice(other_moves) if other_moves else best_move

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

    # def _minimax(self, board, depth, is_maximizing):
    #     """Minimax algorithm implementation"""
    #     score = self._evaluate(board)
        
    #     # If we have a winner or draw
    #     if score is not None:
    #         return score

    #     if is_maximizing:
    #         best = float('-inf')
    #         for i in range(3):
    #             for j in range(3):
    #                 if board[i][j] is None:
    #                     board[i][j] = 0  # O's move
    #                     best = max(best, self._minimax(board, depth + 1, False))
    #                     board[i][j] = None
    #         return best
    #     else:
    #         best = float('inf')
    #         for i in range(3):
    #             for j in range(3):
    #                 if board[i][j] is None:
    #                     board[i][j] = 1  # X's move
    #                     best = min(best, self._minimax(board, depth + 1, True))
    #                     board[i][j] = None
    #         return best
    
    def _minimax(self, board, depth, is_maximizing):
        """Modified: Added depth limitation"""
        score = self._evaluate(board)
        
        # Terminal conditions - added depth check
        if score is not None or depth >= self.config['max_depth']:
            return score if score is not None else self._evaluate_position(board)
        
        if is_maximizing:
            best = float('-inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] is None:
                        board[i][j] = 0
                        best = max(best, self._minimax(board, depth + 1, False))
                        board[i][j] = None
            return best
        else:
            best = float('inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] is None:
                        board[i][j] = 1
                        best = min(best, self._minimax(board, depth + 1, True))
                        board[i][j] = None
            return best

    # New: Added position evaluation for non-terminal states
    def _evaluate_position(self, board):
        """Simple heuristic evaluation for non-terminal positions"""
        center = 3 if board[1][1] == 0 else -3 if board[1][1] == 1 else 0
        corners = sum(2 if board[i][j] == 0 else -2 if board[i][j] == 1 else 0 
                     for i, j in [(0,0), (0,2), (2,0), (2,2)])
        return center + corners

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