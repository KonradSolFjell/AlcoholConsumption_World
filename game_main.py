import tkinter as tk
from tkinter import messagebox
from Lese_Inn import lese_inn
from Remove_Chars import remove_chars
import random
csv_data = lese_inn("alc_consumption_liters_per_capita.csv")


class TipsyTriviaGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Tipsy Trends Trivia")

        self.score = 0
        self.round_number = 1
        self.csv_data = csv_data
        self.current_country = remove_chars(str(random.sample(csv_data.keys(), 1)), "'[]")
        self.countries_played = []

        self.label = tk.Label(root, text="Welcome to Tipsy Trends!")
        self.label.pack(pady=10)

        self.prompt_label = tk.Label(root, text=f"Guess if alcohol consumption in different countries have increased, decreased, or remained the same in a given interval. Difficulties represent the width of the intervals, where harder difficulties mean smaller intervals.")
        self.prompt_label.pack(pady=10)

        self.easy_button = tk.Button(root, text="Easy", command=lambda: self.set_difficulty("easy"))
        self.easy_button.pack(pady=5)

        self.medium_button = tk.Button(root, text="Medium", command=lambda: self.set_difficulty("medium"))
        self.medium_button.pack(pady=5)

        self.hard_button = tk.Button(root, text="Hard", command=lambda: self.set_difficulty("hard"))
        self.hard_button.pack(pady=5)

        self.update_display()

    def game_init(self, root):

        self.easy_button.pack_forget()
        self.medium_button.pack_forget()
        self.hard_button.pack_forget()

        self.increase_button = tk.Button(root, text="Increased", command=lambda: self.check_answer("increased"))
        self.increase_button.pack(pady=5)

        self.decrease_button = tk.Button(root, text="Decreased", command=lambda: self.check_answer("decreased"))
        self.decrease_button.pack(pady=5)

        self.same_button = tk.Button(root, text="Remained the Same", command=lambda: self.check_answer("same"))
        self.same_button.pack(pady=5)

    def check_answer(self, user_guess):
        self.countries_played.append(self.current_country)
        messagebox.showinfo("Result", f"Your guess: {user_guess}\nCorrect!")
        # Update the display for the next round
        self.round_number += 1

        if (self.round_number % 2 == 0):
            self.last_country = self.current_country  # Store the last introduced country
            self.current_country = self.select_new_country()
            self.prompt_label.config(text=f"Round {self.round_number}: Guess if alcohol consumption is higher or lower in {self.last_country} than in {self.current_country}")
        else:
            self.prompt_label.config(text=f"Round {self.round_number}: Guess if alcohol consumption in {self.current_country} is higher, lower or the same in {'YEAR'} as in {'OTHER_YEAR'}.")

        self.update_display()

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty
        self.prompt_label.config(text=f"Round {self.round_number}: Guess if alcohol consumption in {self.current_country} is higher, lower or the same in {'YEAR'} as in {'OTHER_YEAR'}.")
        self.game_init(root)

    def select_new_country(self):
        current_country = remove_chars(str(random.sample(csv_data.keys(), 1)), "'[]")
        while current_country in self.countries_played:
            current_country = remove_chars(str(random.sample(csv_data.keys(), 1)), "'[]")
        return current_country

    def update_display(self):
        self.root.update()

if __name__ == "__main__":
    root = tk.Tk()
    game = TipsyTriviaGame(root)
    root.mainloop()