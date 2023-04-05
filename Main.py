import tkinter as tk
from tkinter import messagebox
import random

def get_list_of_words(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read().splitlines()

def select_word():
    while True:
        word = random.choice(get_list_of_words('/usr/share/dict/words')).lower()
        if len(word) <= 6:
            continue
        else:
            return word

def display_word():
    displayed_word = ""
    for letter in current_word:
        if letter in guessed_letters:
            displayed_word += letter
        else:
            displayed_word += "_"
    return displayed_word

def show_image(index):
    global remaining_tries, image_label
    image_label.config(image=images[index])

def update_display():
    word_label.configure(text=display_word())
    display_remaining_tries()
    show_image(remaining_tries)

def display_remaining_tries():
    remaining_label.configure(text=f"Remaining tries: {remaining_tries}")

def check_game_over():
    if remaining_tries == 0:
        letter_entry.configure(state="disabled")
        show_image(0)
        # doesn't work properly without after() method
        root.after(1, lambda: messagebox.showinfo(message=f"You lost! The word was: \n{current_word}"))
        return True
    elif "_" not in display_word():
        letter_entry.configure(state="disabled")
        root.after(1, lambda: messagebox.showinfo(message="You won!"))
        return True
    else:
        return False

def check_letter(letter):
    global remaining_tries
    if letter in current_word:
        guessed_letters.add(letter)
    else:
        remaining_tries -= 1

def process_try():
    letter = letter_entry.get()
    if len(letter) == 1 and letter.isalpha():
        check_letter(letter)
        update_display()
        show_image(remaining_tries)
        if check_game_over():
            play_button.configure(state="disabled")
    letter_entry.delete(0, tk.END)

root = tk.Tk()
root.title("Hangman")
root.geometry("800x600")

images = [
    tk.PhotoImage(file="images/Hangman-6.png"),
    tk.PhotoImage(file="images/Hangman-5.png"),
    tk.PhotoImage(file="images/Hangman-4.png"),
    tk.PhotoImage(file="images/Hangman-3.png"),
    tk.PhotoImage(file="images/Hangman-2.png"),
    tk.PhotoImage(file="images/Hangman-1.png"),
    tk.PhotoImage(file="images/Hangman-0.png")
]

remaining_tries = 6
guessed_letters = set()
current_word = select_word()

play_button = tk.Button(root, text='Try', command=process_try)
play_button.pack()

word_label = tk.Label(root, text=display_word())
word_label.pack()

remaining_label = tk.Label(root, text=f"Remaining tries: {remaining_tries}")
remaining_label.pack()

image_label = tk.Label()
image_label.pack()
show_image(remaining_tries)

letter_entry = tk.Entry(root)
letter_entry.pack()

rules = tk.Label(text="Hangman is a simple word guessing game. \n"
                      "Players try to figure out an unknown word by guessing letters. \n"
                      "If too many letters which do not appear in the word are guessed, the player is hanged")
rules.pack()
root.mainloop()