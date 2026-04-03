"""
Floor buttons for an elevator
"""

from guizero import App, Box, PushButton, Text

buttons = {}  # Dictionary of pushbutton widgets


def floor_button_pressed(floor):
    """ Function called when the floor button is pressed """
    print(f"Floor {floor} button pressed")
    buttons[floor].bg = "yellow"


def clear_buttons():
    """ Clear all buttons pressed """
    for button in buttons.values():
        button.bg = None


def main():
    app = App(title="Elevator Buttons", width=300, height=650, bg="#ffffff")
    app.text_size = 14
    app.text_bold = True

    Box(app, width=10, height=40, border=False)  # Spacer

    button_box = Box(app, width=100, height=470, border=True)
    Text(button_box, text="Floors")

    for floor in range(6, 0, -1):
        # Create button objects and store them in a dictionary
        btn = PushButton(button_box, text=str(floor),
                         command=floor_button_pressed, args=[floor])
        buttons[floor] = btn
        Box(button_box, width=10, height=10, border=False)  # Spacer

    # Pushbutton to clear all floors
    Box(app, width=10, height=40, align='bottom', border=False)  # Spacer
    PushButton(app, text="CLEAR", align='bottom', command=clear_buttons)

    app.display()


if __name__ == "__main__":
    main()
