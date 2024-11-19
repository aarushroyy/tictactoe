from bots.minimax_bot import MinimaxBot

class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]  # A list to represent the board
        self.current_winner = None  # Keep track of the winner!

    def print_board(self):
        for i in range(3):
            print('|'.join(self.board[i*3:(i+1)*3]))
            if i < 2:
                print('-' * 5)

    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def empty_squares(self):
        return ' ' in self.board

    def make_move(self, square, letter):
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def winner(self, square, letter):
        # Check the row
        row_ind = square // 3
        row = self.board[row_ind*3:(row_ind+1)*3]
        if all([spot == letter for spot in row]):
            return True

        # Check column
        col_ind = square % 3
        column = [self.board[col_ind+i*3] for i in range(3)]
        if all([spot == letter for spot in column]):
            return True

        # Check diagonals
        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]]
            if all([spot == letter for spot in diagonal1]):
                return True
            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            if all([spot == letter for spot in diagonal2]):
                return True
        return False

    def get_board_2d(self):
        """Convert 1D board to 2D for bot interface"""
        return [self.board[i:i+3] for i in range(0, 9, 3)]

    def play_game(self, player1, player2):
        """
        Player1 and Player2 can be:
        - 'human'
        - Bot instance (MinimaxBot or RLBot)
        """
        print("\nGame starting...")
        self.print_board()

        current_player = 'X'
        while self.empty_squares():
            # Get the current player's move
            if current_player == 'X':
                if player1 == 'human':
                    square = self._get_human_move()
                else:  # Bot move
                    row, col = player1.get_move(self.get_board_2d())
                    square = row * 3 + col
            else:
                if player2 == 'human':
                    square = self._get_human_move()
                else:  # Bot move
                    row, col = player2.get_move(self.get_board_2d())
                    square = row * 3 + col

            # Make the move
            if self.make_move(square, current_player):
                print(f"\nPlayer {current_player} makes a move to square {square}")
                self.print_board()

                if self.current_winner:
                    print(f"\nPlayer {current_player} wins!")
                    return current_player

                # Switch players
                current_player = 'O' if current_player == 'X' else 'X'

        print("\nIt's a tie!")
        return None

    def _get_human_move(self):
        """Get and validate human player move"""
        valid_square = False
        square = None
        while not valid_square:
            try:
                square = int(input('Enter your move (0-8): '))
                if square not in self.available_moves():
                    raise ValueError
                valid_square = True
            except ValueError:
                print('Invalid square. Try again.')
        return square

def create_bot(bot_type, difficulty):
    """Factory function to create bots"""
    if bot_type.lower() == 'minimax':
        return MinimaxBot(difficulty)
    else:
        raise ValueError("Invalid bot type. Only 'minimax' is supported")

def main():
    while True:
        print("\nWelcome to Tic Tac Toe!")
        print("1. Player vs Bot")
        print("2. Player vs Player")
        print("3. Bot vs Bot")
        print("4. Quit")
        
        choice = input("\nSelect game mode (1-4): ")
        
        if choice == '4':
            break
            
        game = TicTacToe()
        
        if choice == '1':
            # print("\nSelect bot type:")
            # print("1. Minimax Bot")
            # print("2. Reinforcement Learning Bot")
            # bot_choice = input("Enter choice (1-2): ")
            
            print("\nSelect difficulty:")
            print("1. Easy")
            print("2. Medium")
            print("3. Hard")
            difficulty = input("Enter difficulty (1-3): ")
            
            # Convert difficulty choice to string
            difficulty_map = {'1': 'easy', '2': 'medium', '3': 'hard'}
            bot_type = 'minimax' 
            
            bot = create_bot(bot_type, difficulty_map[difficulty])
            game.play_game('human', bot)
            
        elif choice == '2':
            game.play_game('human', 'human')
            
        elif choice == '3':
            print("\nSelect bot types and difficulties:")
            
            # Bot 1 setup
            print("\nBot 1:")
            # print("1. Minimax Bot")
            # print("2. Reinforcement Learning Bot")
            # bot1_choice = input("Enter choice (1-2): ")
            print("\nSelect difficulty:")
            print("1. Easy")
            print("2. Medium")
            print("3. Hard")
            bot1_diff = input("Enter difficulty (1-3): ")
            
            # Bot 2 setup
            print("\nBot 2:")
            # print("1. Minimax Bot")
            # print("2. Reinforcement Learning Bot")
            # bot2_choice = input("Enter choice (1-2): ")
            print("\nSelect difficulty:")
            print("1. Easy")
            print("2. Medium")
            print("3. Hard")
            bot2_diff = input("Enter difficulty (1-3): ")
            
            difficulty_map = {'1': 'easy', '2': 'medium', '3': 'hard'}
            bot1_type = 'minimax'
            bot2_type = 'minimax' 
            
            bot1 = create_bot(bot1_type, difficulty_map[bot1_diff])
            bot2 = create_bot(bot2_type, difficulty_map[bot2_diff])
            
            game.play_game(bot1, bot2)

if __name__ == '__main__':
    main()