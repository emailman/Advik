import random
from guizero import App, Box, Text, TextBox, PushButton

GREEN = "#6aaa64"
YELLOW = "#c9b458"
GRAY = "#787c7e"
WHITE = "#ffffff"
BORDER = "#d3d6da"

# Game state
target_word = ""
current_row = 0
game_over = False


def main():

    # Load the list of words
    with open("words.txt") as f:
        words = [line.strip() for line in f if line.strip()]

    def check_guess(guess, target):
        colors = [GRAY] * 5
        remaining = list(target)

        # First pass: greens
        for i in range(5):
            if guess[i] == target[i]:
                colors[i] = GREEN
                remaining[remaining.index(guess[i])] = None

        # Second pass: yellows
        for i in range(5):
            if colors[i] == GREEN:
                continue
            if guess[i] in remaining:
                colors[i] = YELLOW
                remaining[remaining.index(guess[i])] = None

        return colors

    def begin_play():
        global target_word, game_over, current_row

        target_word = random.choice(words)
        current_row = 0
        game_over = False
        for cells in grid:
            for box, letter in cells:
                box.bg = WHITE
                letter.value = ""
        status_text.value = ""
        guess_input.value = ""
        guess_input.focus()

    def submit_guess():
        global current_row, game_over

        if game_over:
            return

        guess = guess_input.value.strip().lower()

        if len(guess) != 5 or not guess.isalpha():
            status_text.value = "Enter a valid 5-letter word."
            return

        colors = check_guess(guess, target_word)

        for i, (box, letter) in enumerate(grid[current_row]):
            letter.value = guess[i].upper()
            box.bg = colors[i]

        current_row += 1
        guess_input.value = ""

        if all(c == GREEN for c in colors):
            # If all letters are GREEN, you won
            status_text.value = "You win!"
            game_over = True
        elif current_row == 6:
            # If you failed in 6 guesses, you lost
            status_text.value = \
                f"Game over! The word was: {target_word.upper()}"
            game_over = True
        else:
            status_text.value = ""

    def on_key(event):
        # Submit a guess if used typed <enter>
        if event.key == "\r":
            submit_guess()

    # Build UI
    app = App(title="Wordle", width=360, height=550, bg="#ffffff")
    app.text_size = 14

    Text(app, text="WORDLE", size=24, font="Arial",
         bold=True, color="#000000")

    grid_box = Box(app, layout="grid", border=False)
    grid = []

    # Draw a grid of 6 rows amd 5 columns
    for row in range(6):
        row_cells = []
        for col in range(5):
            cell_box = Box(grid_box, grid=[col, row],
                           width=52, height=52, border=2)
            cell_box.bg = WHITE
            cell_box.text_color = BORDER
            letter_text = Text(cell_box, text="", size=22,
                               font="Arial", bold=True, color="#000000")
            row_cells.append((cell_box, letter_text))
        grid.append(row_cells)

    Box(app, height=12, width=1)  # spacer

    input_row = Box(app, layout="auto", align="top")
    guess_input = TextBox(input_row, width=14, align="left")
    guess_input.when_key_pressed = on_key
    guess_input.focus()

    Box(input_row, width=8, height=1, align="left")  # spacer

    PushButton(input_row, text="Guess", command=submit_guess,
               align="left")

    status_text = Text(app, text="", color="#cc0000", size=12)

    button_row = Box(app, layout="auto", align="top")
    PushButton(button_row, text="Play Again", command=begin_play,
               align="left")

    Box(button_row, width=8, height=1, align="left")  # spacer

    PushButton(button_row, text="Quit", command=app.destroy,
               align="left")

    begin_play()

    app.display()


if __name__ == '__main__':
    main()
