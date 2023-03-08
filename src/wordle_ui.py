import tkinter as tk
import tkinter.messagebox
from functools import partial

from game_status import GameStatus
from match import Match
from spell_checker import is_spelling_correct
from word_picker import get_a_random_word
from wordle import play

WORD_SIZE = 5
ALLOWED_ATTEMPTS = 6
MEDIUM_GRAY = "#BBB"


def create_window(target_word):
    window = tk.Tk()
    window.title("Wordle")
    cells = []

    input_grid_frame = tk.Frame(window, background="gray")
    input_grid_frame.pack()

    guess_btn_frame = tk.Frame(window)
    guess_btn_frame.pack()
    guess_btn = tk.Button(guess_btn_frame, text="Guess!", state="disabled", font=('Times', 20, 'bold'),
                          disabledforeground='gray')
    guess_btn.pack()

    for i in range(ALLOWED_ATTEMPTS):
        cells.append([])
        row_color = "white" if i == 0 else MEDIUM_GRAY
        for j in range(WORD_SIZE):
            label = tk.Label(input_grid_frame, width=4, font=('Times', 20, 'bold'), justify='center', fg='black',
                             bg=row_color)
            label.grid(row=i, column=j, padx=4, pady=5)
            cells[-1].append(label)

    guess_btn_cmd = partial(guess_btn_action, target_word, cells, guess_btn, window)
    guess_btn.configure(command=guess_btn_cmd)
    window.bind('<KeyPress>', lambda e, *_: letter_entered(e, cells, guess_btn))
    window.bind('<BackSpace>', lambda *_: backspace_pressed(cells, guess_btn))
    window.bind('<Return>', lambda *_: return_key_pressed(target_word, cells, guess_btn, window))

    return window, cells, guess_btn


def set_guess_btn_enabled(guess_btn, enabled):
    button_state = "normal" if enabled else "disabled"
    guess_btn.config(state=button_state)


def set_label_row_enabled(row, label, enabled):
    input_row_state = "white" if enabled else MEDIUM_GRAY
    for i in range(WORD_SIZE):
        label[row][i].config(bg=input_row_state)


def letter_entered(event, cells, guess_btn):
    char = str(event.char)
    current_row = find_the_current_row(cells)
    if current_row < ALLOWED_ATTEMPTS:
        current_cell = find_the_current_cell(cells, current_row)
        if char.isalpha() and current_cell < WORD_SIZE:
            cells[current_row][current_cell]["text"] = char.upper()
            if current_cell == WORD_SIZE - 1:
                set_guess_btn_enabled(guess_btn, True)


def backspace_pressed(cells, guess_btn):
    current_row = find_the_current_row(cells)
    if current_row < ALLOWED_ATTEMPTS:
        current_cell = find_the_current_cell(cells, current_row)
        if current_cell > 0:
            cells[current_row][current_cell - 1]["text"] = ""
            set_guess_btn_enabled(guess_btn, False)


def return_key_pressed(target_word, cells, guess_btn, window):
    guess_btn_state = str(guess_btn["state"])
    if guess_btn_state == "normal":
        guess_btn_action(target_word, cells, guess_btn, window)


def guess_btn_action(target_word, cells, guess_btn, window):
    # target_word = "FAVOR"

    current_row = find_the_current_row(cells)

    guessed_word = guessed_word_from_current_row(cells, current_row)

    result = play(target_word, guessed_word, current_row, is_spelling_correct)

    if result["game_status"] == GameStatus.WRONG_SPELLING:
        tkinter.messagebox.showinfo("Wrong Spelling", "Wrong Spelling")
        window.focus_force()
        return

    color_guess(result["tally"], cells, current_row)
    set_guess_btn_enabled(guess_btn, False)

    if result["game_status"] == GameStatus.INPROGRESS:
        set_label_row_enabled(current_row + 1, cells, True)

    elif result["game_status"] == GameStatus.WIN or result["game_status"] == GameStatus.LOSE:
        tkinter.messagebox.showinfo("Greeting", result["greeting_message"])
        window.destroy()


def guessed_word_from_current_row(cells, current_row):
    guessed_word = ""

    for i in range(WORD_SIZE):
        guessed_word += cells[current_row][i].cget("text")

    return guessed_word


def find_the_current_cell(labels, row):
    for i in range(WORD_SIZE):
        if len(labels[row][i].cget("text")) == 0:
            return i
    return WORD_SIZE


def find_the_current_row(labels):
    for i in range(ALLOWED_ATTEMPTS):
        if labels[i][0].cget("bg") == "white":
            return i
    return ALLOWED_ATTEMPTS


def color_guess(guess_tally, cells, row):
    for i in range(WORD_SIZE):
        if guess_tally[i] == Match.EXACT:
            cells[row][i].config(bg="green")
        elif guess_tally[i] == Match.PRESENT:
            cells[row][i].config(bg="yellow")
        else:
            cells[row][i].config(bg=MEDIUM_GRAY)


def main():
    target_word = get_a_random_word()

    window, entries, guess_btn = create_window(target_word)
    window.mainloop()


if __name__ == '__main__':
    main()
