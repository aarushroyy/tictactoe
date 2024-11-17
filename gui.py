import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk
import random
from bots.minimax_bot import MinimaxBot
from bots.rl_bot import RLBot


class matrix:
    def __init__(self):
        self.matrix = [[None for _ in range(3)] for _ in range(3)]
    
    def check_win(self):
        # Check rows
        for row in self.matrix:
            if all(cell == 1 for cell in row):
                return 1  # X wins
            if all(cell == 0 for cell in row):
                return 0  # O wins

        # Check columns
        for col in range(3):
            column = [self.matrix[row][col] for row in range(3)]
            if all(cell == 1 for cell in column):
                return 1
            if all(cell == 0 for cell in column):
                return 0

        # Check diagonals
        diag1 = [self.matrix[i][i] for i in range(3)]
        diag2 = [self.matrix[i][2-i] for i in range(3)]
        
        if all(cell == 1 for cell in diag1) or all(cell == 1 for cell in diag2):
            return 1
        if all(cell == 0 for cell in diag1) or all(cell == 0 for cell in diag2):
            return 0

        return None

    def check_draw(self):
        return all(all(cell is not None for cell in row) for row in self.matrix)


class TicTacToeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tic Tac Toe Game")
        self.geometry("400x600")
        self.resizable(False, False)
        self.configure(bg="#D9E4F5")  # Light pastel blue background
        self.pages = {}
        self.current_page = None

        # Initialize pages
        self.add_page(HomePage(self))
        self.add_page(SettingsPage(self))
        self.add_page(GamePage(self))
        self.add_page(BotSettingsPage(self))

        # Show the home page initially
        self.show_page("HomePage")

    def add_page(self, page):
        """Add a page to the app."""
        self.pages[page.page_name] = page

    def show_page(self, page_name):
        """Show the requested page."""
        if self.current_page:
            self.current_page.pack_forget()
        self.current_page = self.pages[page_name]
        self.current_page.pack(fill="both", expand=True)


class HomePage(tk.Frame):
    page_name = "HomePage"

    def __init__(self, master):
        super().__init__(master, bg="#D9E4F5")  # Light pastel blue
        title_font = font.Font(family="Arial Rounded MT Bold", size=20, weight="bold")
        button_font = font.Font(family="Arial", size=14, weight="bold")

        # Title
        tk.Label(self, text="Welcome to Tic Tac Toe", font=title_font, bg="#D9E4F5").pack(pady=30)

        # Logo (Optional)
        try:
            image = Image.open(r"assets/logo.jpg")
            image = image.resize((250, 90), Image.LANCZOS)
            self.photo = ImageTk.PhotoImage(image)
            image_label = tk.Label(self, image=self.photo, bg="#D9E4F5")
            image_label.pack(pady=10)
        except Exception as e:
            tk.Label(self, text="Tic Tac Toe", font=title_font, bg="#D9E4F5").pack(pady=10)

        # Buttons for Game Modes
        tk.Button(self, text="Player vs Bot", font=button_font, bg="#6FA3EF", fg="black",
                  command=lambda: master.show_page("SettingsPage")).pack(pady=15, ipadx=10, ipady=5)
        tk.Button(self, text="Player1 vs Player2", font=button_font, bg="#6FA3EF", fg="black",
                  command=lambda: master.show_page("GamePage")).pack(pady=15, ipadx=10, ipady=5)
        tk.Button(self, text="Bot vs Bot", font=button_font, bg="#6FA3EF", fg="black",
                  command=lambda: master.show_page("BotSettingsPage")).pack(pady=15, ipadx=10, ipady=5)

        # Quit Button
        tk.Button(self, text="Quit", font=button_font, bg="#FF6F61", fg="black",
                  command=master.quit).pack(pady=20, ipadx=20, ipady=5)


class SettingsPage(tk.Frame):
    page_name = "SettingsPage"

    def __init__(self, master):
        super().__init__(master, bg="#D9E4F5")  # Light pastel blue
        title_font = font.Font(family="Arial Rounded MT Bold", size=16, weight="bold")
        option_font = font.Font(family="Arial", size=12)

        tk.Label(self, text="Player vs Bot Settings", font=title_font, bg="#D9E4F5").pack(pady=20)

        # Difficulty selection
        self.difficulty_var = tk.StringVar(value="Medium")
        tk.Label(self, text="Select Bot Difficulty:", font=option_font, bg="#D9E4F5").pack(pady=10)
        difficulties = ["Easy", "Medium", "Hard"]
        for difficulty in difficulties:
            tk.Radiobutton(self, text=difficulty, variable=self.difficulty_var, value=difficulty, bg="#D9E4F5",
                           font=option_font).pack(anchor="w", padx=20, pady=5)

        # Start Game Button
        tk.Button(self, text="Start Game", font=option_font, bg="#6FA3EF", fg="black",
                  command=self.start_game).pack(pady=20, ipadx=20, ipady=5)

        # Back to Home Button
        tk.Button(self, text="Back to Home", font=option_font, bg="#FF6F61", fg="black",
                  command=lambda: master.show_page("HomePage")).pack(pady=10, ipadx=20, ipady=5)

    def start_game(self):
        # for setting the diffculty
        game_page = self.master.pages["GamePage"]
        difficulty = self.difficulty_var.get()  # Easy, Medium, or Hard
        game_page.initialize_game(
            mode="Player vs Bot",
            bot_type="minimax",  # or we can add radio buttons to choose between 'minimax' and 'rl'
            difficulty=difficulty
        )
        
        self.master.show_page("GamePage")

class BotSettingsPage(tk.Frame):
    page_name = "BotSettingsPage"

    def __init__(self, master):
        super().__init__(master, bg="#D9E4F5")
        title_font = font.Font(family="Arial Rounded MT Bold", size=16, weight="bold")
        option_font = font.Font(family="Arial", size=12)

        tk.Label(self, text="Bot vs Bot Settings", font=title_font, bg="#D9E4F5").pack(pady=20)

        # Bot 1 settings
        tk.Label(self, text="Bot 1 (X)", font=title_font, bg="#D9E4F5").pack(pady=10)
        self.bot1_difficulty = tk.StringVar(value="Medium")
        for difficulty in ["Easy", "Medium", "Hard"]:
            tk.Radiobutton(self, text=difficulty, variable=self.bot1_difficulty, value=difficulty, 
                          bg="#D9E4F5", font=option_font).pack(anchor="w", padx=20, pady=5)

        # Bot 2 settings
        tk.Label(self, text="Bot 2 (O)", font=title_font, bg="#D9E4F5").pack(pady=10)
        self.bot2_difficulty = tk.StringVar(value="Medium")
        for difficulty in ["Easy", "Medium", "Hard"]:
            tk.Radiobutton(self, text=difficulty, variable=self.bot2_difficulty, value=difficulty,
                          bg="#D9E4F5", font=option_font).pack(anchor="w", padx=20, pady=5)

        # Start Game Button
        tk.Button(self, text="Start Game", font=option_font, bg="#6FA3EF", fg="black",
                 command=self.start_game).pack(pady=20, ipadx=20, ipady=5)

        # Back to Home Button
        tk.Button(self, text="Back to Home", font=option_font, bg="#FF6F61", fg="black",
                 command=lambda: master.show_page("HomePage")).pack(pady=10, ipadx=20, ipady=5)

    def start_game(self):
        game_page = self.master.pages["GamePage"]
        game_page.initialize_game(
            mode="Bot vs Bot",
            bot1_difficulty=self.bot1_difficulty.get(),
            bot2_difficulty=self.bot2_difficulty.get()
        )
        self.master.show_page("GamePage")
        
class GamePage(tk.Frame):
    page_name = "GamePage"
     
    def __init__(self, master):
        super().__init__(master, bg="#D9E4F5")
        self.mat = matrix()
        self.matrix = self.mat.matrix
        self.X_score = 0
        self.O_score = 0
        self.mode = None
        self.bot_difficulty = "Medium"
        self.turn = "X"
        self.bot1 = None
        self.bot2 = None

        # Setup UI elements
        title_font = font.Font(family="Arial Rounded MT Bold", size=14, weight="bold")
        button_font = font.Font(family="Arial", size=26, weight="bold")

        # Turn label
        self.turn_label = tk.Label(self, text="Player's Turn", font=title_font, bg="#D9E4F5")
        self.turn_label.pack(pady=10)

        # Game grid buttons
        self.buttons = []
        grid_frame = tk.Frame(self, bg="#D9E4F5")
        grid_frame.pack(pady=20)
        
        for row in range(3):
            button_row = []
            for col in range(3):
                button = tk.Button(
                    grid_frame, 
                    text="", 
                    font=button_font,
                    width=3, 
                    height=1,
                    bg="white",
                    fg="black",
                    command=lambda r=row, c=col: self.set_value(r, c)
                )
                button.grid(row=row, column=col, padx=5, pady=5)
                button_row.append(button)
            self.buttons.append(button_row)

        # Score labels
        self.X_score_label = tk.Label(self, text=f"X-Score: {self.X_score}", font=title_font, bg="#D9E4F5")
        self.X_score_label.pack(side="left", padx=20)

        self.O_score_label = tk.Label(self, text=f"O-Score: {self.O_score}", font=title_font, bg="#D9E4F5")
        self.O_score_label.pack(side="right", padx=20)

        # Back button
        tk.Button(self, text="Back to Home", font=title_font, bg="#FF6F61", fg="black",
                  command=self.back_to_home).pack(pady=20)

    def set_winner(self, winner):
        self.turn_label.config(text=f"{winner} Wins!")
        if winner == "X":
            self.X_score += 1
            self.X_score_label.config(text=f"X-Score: {self.X_score}")
        else:
            self.O_score += 1
            self.O_score_label.config(text=f"O-Score: {self.O_score}")
        self._disable_buttons()

    def set_draw(self):
        self.turn_label.config(text="It's a Draw!")
        self._disable_buttons()

    def _disable_buttons(self):
        for row in self.buttons:
            for button in row:
                button.config(state="disabled")

    def back_to_home(self):
        self.reset_game()
        self.master.show_page("HomePage")

    def reset_game(self):
        self.mat = matrix()
        self.matrix = self.mat.matrix
        self.turn = "X"
        for row in self.buttons:
            for button in row:
                button.config(text="", state="normal")
        self.update_turn_label()

    def update_turn_label(self):
        self.turn_label.config(text=f"{self.turn}'s Turn")
    
    def initialize_game(self, mode, bot_type="minimax", difficulty=None, bot1_difficulty=None, bot2_difficulty=None):
        """Initialize the game with proper mode and bot settings"""
        self.mode = mode
        self.reset_game()
        
        if mode == "Player vs Bot":
            self.bot1 = None
            self.bot2 = MinimaxBot(difficulty.lower())
        elif mode == "Bot vs Bot":
            self.bot1 = MinimaxBot(bot1_difficulty.lower())
            self.bot2 = MinimaxBot(bot2_difficulty.lower())
            self.after(1000, self.make_bot_move)
        else:  # Player vs Player
            self.bot1 = None
            self.bot2 = None
        
        self.turn = "X"
        self.update_turn_label()

    def set_value(self, row, col):
        """Handle moves for all game modes"""
        if self.matrix[row][col] is not None or (self.mode == "Bot vs Bot"):
            return

        # Make the move
        current_value = 1 if self.turn == "X" else 0
        self.matrix[row][col] = current_value
        self.buttons[row][col].config(text=self.turn)
        
        # Check for game end
        winner = self.mat.check_win()
        if winner is not None:
            self.set_winner("X" if winner == 1 else "O")
            return
        elif self.mat.check_draw():
            self.set_draw()
            return

        # Handle next move based on game mode
        if self.mode == "Player vs Bot" and self.turn == "X":
            self.turn = "O"
            self.update_turn_label()
            self.after(500, self.make_bot_move)
        else:
            # Player vs Player or after bot's move
            self.turn = "O" if self.turn == "X" else "X"
            self.update_turn_label()

    def make_bot_move(self):
        """Execute bot moves only when in bot modes"""
        # Early return if game is over or not in a bot mode
        if (self.mat.check_win() is not None or 
            self.mat.check_draw() or 
            self.mode not in ["Bot vs Bot", "Player vs Bot"]):
            return
            
        current_bot = None
        if self.mode == "Bot vs Bot":
            current_bot = self.bot1 if self.turn == "X" else self.bot2
        elif self.mode == "Player vs Bot" and self.turn == "O":
            current_bot = self.bot2
        
        if not current_bot:
            return
            
        # Execute bot's move
        bot_row, bot_col = current_bot.get_move(self.matrix)
        if bot_row is not None and bot_col is not None:
            current_value = 1 if self.turn == "X" else 0
            self.matrix[bot_row][bot_col] = current_value
            self.buttons[bot_row][bot_col].config(text=self.turn)
            
            # Check for game end
            winner = self.mat.check_win()
            if winner is not None:
                self.set_winner("X" if winner == 1 else "O")
                return
            elif self.mat.check_draw():
                self.set_draw()
                return
                
            # Switch turns
            self.turn = "O" if self.turn == "X" else "X"
            self.update_turn_label()
            
            # Schedule next bot move if in Bot vs Bot mode
            if self.mode == "Bot vs Bot":
                self.after(1000, self.make_bot_move)

    def reset_game(self):
        self.mat = matrix()
        self.matrix = self.mat.matrix
        self.turn = "X"
        for row in self.buttons:
            for button in row:
                button.config(text="", state="normal")
        self.update_turn_label()

    def update_turn_label(self):
        """Update the turn label based on game mode"""
        if self.mode == "Player vs Bot":
            self.turn_label.config(text="Your Turn" if self.turn == "X" else "Bot's Turn")
        elif self.mode == "Bot vs Bot":
            self.turn_label.config(text=f"Bot {self.turn}'s Turn")
        else:  # Player vs Player
            self.turn_label.config(text=f"Player {self.turn}'s Turn")
        
        
if __name__ == "__main__":
    app = TicTacToeApp()
    app.mainloop()
