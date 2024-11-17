from abc import ABC, abstractmethod

class BotInterface(ABC):
    """Base interface for all bot implementations"""
    def __init__(self, difficulty='medium'):
        self.difficulty = difficulty.lower()
        
    @abstractmethod
    def get_move(self, board):
        """
        Get the next move from the bot
        Args:
            board: Current game board state
        Returns:
            tuple: (row, col) for the next move
        """
        pass

    def _convert_position_to_coordinates(self, position):
        """Convert a 0-8 position to row,col coordinates"""
        row = position // 3
        col = position % 3
        return row, col

    def _convert_coordinates_to_position(self, row, col):
        """Convert row,col coordinates to 0-8 position"""
        return row * 3 + col