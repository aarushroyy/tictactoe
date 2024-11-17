from gui import TicTacToeApp
from bots.minimax_bot import MinimaxBot
from bots.rl_bot import RLBot

def main():
    # Create the application
    app = TicTacToeApp()
    
    # Configure window properties
    app.title("Tic Tac Toe")
    app.geometry("400x600")
    app.resizable(False, False)
    
    # Start the application
    app.mainloop()

if __name__ == "__main__":
    main()