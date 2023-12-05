import tkinter as tk
from tkinter import messagebox
from Lese_Inn import lese_inn
from Remove_Chars import remove_chars
import random
csv_data = lese_inn("alc_consumption_liters_per_capita.csv")

class TipsyTriviaGame:
    def __init__(self, root):
        #Defining window, window title and resolution
        self.root = root
        self.root.title("Tipsy Trivia")
        self.root.geometry("700x300")

        #Defining necessary game variables
        self.round_number = 1
        self.csv_data = csv_data
        self.current_country = remove_chars(str(random.sample(list(csv_data.keys()), 1)), "'[]")
        self.countries_played = []
        self.player_hp = 5

        #Creating main menu and displaying it
        self.label = tk.Label(root, text="Welcome to Tipsy Trivia!")
        self.label.pack(pady=10)

        self.prompt_label = tk.Label(root, text=f"Guess if alcohol consumption in different countries have increased, decreased, or remained the same in a given interval. \nDifficulties represent the width of the intervals, where harder difficulties mean smaller intervals.")
        self.prompt_label.pack(pady=10)

        self.easy_button = tk.Button(root, text="Easy", command=lambda: self.set_difficulty("easy"))
        self.easy_button.pack(pady=5)

        self.medium_button = tk.Button(root, text="Medium", command=lambda: self.set_difficulty("medium"))
        self.medium_button.pack(pady=5)

        self.hard_button = tk.Button(root, text="Hard", command=lambda: self.set_difficulty("hard"))
        self.hard_button.pack(pady=5)

        self.update_display()

    def game_init(self, root):
        
        #Hiding main menu buttons, could've used a generic function to hide all elements but decided against it as the code doesn't call pack_forget() all too much
        self.easy_button.pack_forget()
        self.medium_button.pack_forget()
        self.hard_button.pack_forget()

        #Calling select_years() here because it's the first round and advance_round() (which also contains select_years()) hasn't been called yet
        self.years = self.select_years(self.difficulty)

        #Configuring and creating game menu elements with the buttons calling check_answer() with their respective statements as paramterers. Also constructing buttons that will only be needed in the second round (but not displaying them), just because I figured it was a convenient place to do so. 
        self.health_label = tk.Label(root, text=f"Your HP: {self.player_hp}")
        self.health_label.pack(pady=5)

        self.label.config(text="Tipsy Trivia")
        self.prompt_label.config(text=f"Round {self.round_number}: Guess if alcohol consumption in {self.current_country} has increased, decreased or stayed the same from {self.years[0]} to {self.years[1]}.")

        self.increase_button = tk.Button(root, text="Increased", command=lambda: self.check_answer("Increased"))
        self.increase_button.pack(pady=5)

        self.decrease_button = tk.Button(root, text="Decreased", command=lambda: self.check_answer("Decreased"))
        self.decrease_button.pack(pady=5)

        self.stayed_the_same_button = tk.Button(root, text="Stayed the same", command=lambda: self.check_answer("Stayed the same"))
        self.stayed_the_same_button.pack(pady=5)

        self.higher_button = tk.Button(root, text="Higher", command=lambda: self.check_answer("Higher"))
        self.lower_button = tk.Button(root, text="Lower", command=lambda: self.check_answer("Lower"))
        self.same_button = tk.Button(root, text="Same", command=lambda: self.check_answer("Same"))

    def correct_answer(self, type_of_answer):
        #Checks what type of answer the guess is and checks accordingly whether or not it's the correct answer. Here it returns a string, just because that's the most convenient with the way check_answer(), the buttons and the user_guess variable are implemented.
        if type_of_answer == "same country":
            alc_consumption_1 = float(self.current_country_data[f"{self.years[0]}"])
            alc_consumption_2 = float(self.current_country_data[f"{self.years[1]}"])
            if -0.5 < alc_consumption_1 - alc_consumption_2 < 0.5 :
                return "Stayed the same"
            elif alc_consumption_1 < alc_consumption_2:
                return "Increased"
            elif alc_consumption_1 > alc_consumption_2:
                return "Decreased"
        elif type_of_answer == "two countries":
            alc_consumption_1 = float(self.last_country_data[(self.years[0])])
            alc_consumption_2 = float(self.current_country_data[(self.years[0])])
            if -0.5 < alc_consumption_1 - alc_consumption_2 < 0.5:
                return "Same"
            elif alc_consumption_1 < alc_consumption_2:
                return "Lower"
            elif alc_consumption_1 > alc_consumption_2:
                return "Higher"
    
    def check_answer(self, user_guess):
        #Sends a type_of_answer (based on the type of guess as they are distinct for the two types of questions) as a parameter to correct_answer(). Checks if the string sent by the button is the same as the string correct_answer() returns for each type of answer respectively. Only shows a dialog box if the guess is correct and both shows a dialog box and drains HP if the guess is wrong. If the HP drops to 0 the game is over, a dialog box is shown and the window is closed.
        if user_guess == "Stayed the same" or user_guess == "Increased" or user_guess == "Decreased":
            if self.correct_answer("same country") == user_guess:
                messagebox.showinfo("Result", f"Your guess: {user_guess}\nCorrect!")
            else:
                messagebox.showinfo("Result", f"Your guess: {user_guess}\nIncorrect!")
                self.player_hp -= 1
                if self.player_hp <= 0:
                    messagebox.showinfo("Game Over", f"You ran out of health. You got {self.round_number-5} questions correct!")
                    self.root.destroy()
                    return
        elif user_guess == "Same" or user_guess == "Lower" or user_guess == "Higher":
            if self.correct_answer("two countries") == user_guess:
                messagebox.showinfo("Result", f"Your guess: {user_guess}\nCorrect!")
            else:
                messagebox.showinfo("Result", f"Your guess: {user_guess}\nIncorrect!")
                self.player_hp -= 1
                if self.player_hp <= 0:
                    messagebox.showinfo("Game Over", "You ran out of health. Game over!")
                    self.root.destroy()
                    return
                
        self.advance_round()

    def advance_round(self):
        #Adds the country that was just played to countries_played so the countries don't repeat and increments the round number.
        self.countries_played.append(self.current_country)
        self.round_number += 1

        #First if-block executes if the round is even-numbered (every other round), second executes on odd numbers. Even-numbered rounds show two countries, so the last_country variable is defined to carry over the country that was last introduced to the next round. Then a new country is selected. A current and last_country_data variable is defined for readability's sake. The buttons are hidden and shown respectively. Could end up with a memory leak? Unsure how Tkinter handles this. 
        if (self.round_number % 2 == 0):
            self.last_country = self.current_country 
            self.last_country_data = csv_data[self.last_country]
            self.current_country = self.select_new_country()
            self.current_country_data = csv_data[self.current_country]
            
            self.prompt_label.config(text=f"Round {self.round_number}: Guess if alcohol consumption is higher or lower in {self.last_country} than in {self.current_country}")

            self.increase_button.pack_forget()
            self.decrease_button.pack_forget()
            self.stayed_the_same_button.pack_forget()
            
            self.higher_button.pack(pady=5)
            self.lower_button.pack(pady=5)
            self.same_button.pack(pady=5)
        else:
            self.years = self.select_years(self.difficulty)

            self.prompt_label.config(text=f"Round {self.round_number}: Guess if alcohol consumption in {self.current_country} has increased, decreased or stayed the same from {self.years[0]} to {self.years[1]}.")

            self.higher_button.pack_forget()
            self.lower_button.pack_forget()
            self.same_button.pack_forget()

            self.increase_button.pack(pady=5)
            self.decrease_button.pack(pady=5)
            self.stayed_the_same_button.pack(pady=5)

        self.health_label.config(text=f"Player HP: {self.player_hp}")

        self.update_display()
    
    def select_years(self, difficulty):
        self.current_country_data = csv_data[self.current_country]
        if difficulty == "easy":
            #Selects the first and last year from that country's data.
            year_1, *_ = self.current_country_data.keys()
            year_2, *_ = reversed(self.current_country_data.keys())
        elif difficulty == "medium":
            #Selects the first year in the dataset and the third last element, in most cases resulting in an interval of 3x5 years. Some countries only have data for 3 or 2 years, in which case the second if-test fires and tightens the interval to one where it would fit the data. This is a rather extreme edge case (one country in the dataset only has data for 2 years) and so further optimizations have not been done.
            year_1 = list(self.current_country_data.keys())[0]
            year_2 = list(self.current_country_data.keys())[-3]
            if year_1 == year_2:
                year_1 = list(self.current_country_data.keys())[0]
                year_2 = list(self.current_country_data.keys())[-1]
        else:
            #Selects a random year from the data, tries to select the year above this year in the data, and if that fails (out of index), lower the first year and select the year above that one.
            year_1 = remove_chars(str(random.sample(list(self.current_country_data.keys()), 1)), "[']")
            try:
                year_2 = list(self.current_country_data.keys())[list(self.current_country_data.keys()).index(f"{year_1}")+1]
            except IndexError:
                year_1 = list(self.current_country_data.keys())[list(self.current_country_data.keys()).index(f"{year_1}")-1]
                year_2 = list(self.current_country_data.keys())[list(self.current_country_data.keys()).index(f"{year_1}")+1]
        #Returns the years in a tuple with the outer characters removed.        
        return remove_chars(year_1, "[']"), remove_chars(year_2, "[']")
        
    def set_difficulty(self, difficulty):
        #Saves the difficulty in a variable
        self.difficulty = difficulty
        self.game_init(root)

    def select_new_country(self):
        #Selects new country by only using the keys (countries) of the data, which is a dictionary.  
        current_country = remove_chars(str(random.sample(list(csv_data.keys()), 1)), "'[]")
        #Selects new country if the country is in the countries_played list
        while current_country in self.countries_played:
            current_country = remove_chars(str(random.sample(list(csv_data.keys()), 1)), "'[]")
        return current_country

    def update_display(self):
        self.root.update()

if __name__ == "__main__":
    root = tk.Tk()
    game = TipsyTriviaGame(root)
    root.mainloop()
