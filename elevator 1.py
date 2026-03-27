"""
Floor buttons for an elevator
"""

from guizero import App, Box, PushButton, Text

buttons = {}  # Set of pushbutton widgets


def main():

    def floor_button_pressed(_floor):
        """ Function called when the floor button is pressed """
        print(f"Floor {_floor} button pressed")
        buttons[_floor].bg = "yellow"

    def clear_buttons():
        """ Clear all buttons pressed """
        for _btn in buttons.values():
            _btn.bg = None

    app = App(title="Elevator", width=300, height=650, bg="#ffffff")
    app.text_size = 14
    app.text_bold = True

    Box(app, width=10, height=40, border=False)  # Spacer

    button_box = Box(app, width=100, height=470, border=True)
    Text(button_box, text="Floors")

    for floor in range(6, 0, -1):
        # Create button objects and store them in a set
        btn = PushButton(button_box, text=str(floor),
                         command=floor_button_pressed, args=[floor])
        buttons[floor] = btn
        Box(button_box, width=10, height=10, border=False)  # Spacer

    # Pushbutton to clear all selected floors
    Box(app, width=10, height=40, align='bottom', border=False)  # Spacer
    PushButton(app, text="CLEAR", align='bottom', command=clear_buttons)

    app.display()


if __name__ == "__main__":
    main()
