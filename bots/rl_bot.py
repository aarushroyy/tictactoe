import numpy as np
import random
from .bot_interface import BotInterface

class RLBot(BotInterface):
    def __init__(self, difficulty='medium'):
        super().__init__(difficulty)
        # Load pre-trained weights based on difficulty
        self.state_values = self._load_weights()
        
        # Set exploration rate based on difficulty
        if self.difficulty == 'easy':
            self.epsilon = 0.7  # More random moves
        elif self.difficulty == 'medium':
            self.epsilon = 0.3  # Balance between random and trained moves
        else:  # hard
            self.epsilon = 0.0  # Always use trained moves
            
    def get_move(self, board):
        # Convert board to the format used in training
        state = self._convert_board_format(board)
        
        # Get available moves
        empty_cells = []
        for i in range(3):
            for j in range(3):
                if board[i][j] is None:
                    empty_cells.append((i, j))
                    
        # For easy mode, higher chance of random move
        if self.difficulty == 'easy' and random.random() < self.epsilon:
            return random.choice(empty_cells) if empty_cells else None
            
        # Calculate values for each possible move
        move_values = []
        moves = []
        
        for row, col in empty_cells:
            new_state = [row[:] for row in state]
            new_state[row][col] = 'O'
            moves.append((row, col))
            move_values.append(self._get_state_value(new_state))
            
        if not moves:
            return None
            
        # For medium difficulty, sometimes choose suboptimal moves
        if self.difficulty == 'medium' and random.random() < self.epsilon:
            return random.choice(moves)
            
        # Choose best move
        best_move_idx = np.argmax(move_values)
        return moves[best_move_idx]
        
    def _load_weights(self):
        try:
            if self.difficulty == 'easy':
                return np.loadtxt('weights/rl_weights_easy.txt')
            elif self.difficulty == 'medium':
                return np.loadtxt('weights/rl_weights_medium.txt')
            else:
                return np.loadtxt('weights/rl_weights_hard.txt')
        except:
            # If weights file not found, return default weights
            return np.zeros((19683,))  # 3^9 possible states
            
    def _convert_board_format(self, board):
        """Convert the game board to the format used in training"""
        return [[' ' if cell is None else cell for cell in row] for row in board]
        
    def _get_state_value(self, state):
        """Get the value of a state from the trained weights"""
        # Convert state to index
        state_str = ''.join([''.join(row) for row in state])
        state_idx = self._state_to_index(state_str)
        return self.state_values[state_idx]
        
    def _state_to_index(self, state_str):
        """Convert state string to index in the weights array"""
        base3 = 0
        for i, char in enumerate(state_str):
            if char == 'X':
                value = 0
            elif char == 'O':
                value = 1
            else:
                value = 2
            base3 += value * (3 ** i)
        return base3