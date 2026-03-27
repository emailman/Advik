"""
Elevator shaft and elevator cab drawing
"""

from guizero import App, Drawing

# Elevator Shaft Geometry
SHAFT_LEFT = 150
SHAFT_RIGHT = 350
SHAFT_TOP = 50
FLOOR_COUNT = 6
FLOOR_HEIGHT = 83
SHAFT_BOTTOM = SHAFT_TOP + FLOOR_COUNT * FLOOR_HEIGHT

BORDER = 3  # outline width in pixels


def floor_top(floor):
    """ Return the y coordinate of the top edge of the given floor
     (1=bottom, 6=top) """
    return SHAFT_TOP + (FLOOR_COUNT - floor) * FLOOR_HEIGHT


def main():
    app = App(title="Elevator Shaft", width=450, height=620, bg="white")

    # Use the whole app window for drawing
    d = Drawing(app, width=450, height=620)

    # --- floor rectangles (brown fill, no outline) and labels ---
    for floor in range(1, FLOOR_COUNT + 1):
        y = floor_top(floor)
        d.rectangle(SHAFT_LEFT, y, SHAFT_RIGHT, y + FLOOR_HEIGHT,
                    color="brown", outline=False)

        # label to the left of the shaft,
        # vertically centred in the floor band
        label_y = y + FLOOR_HEIGHT // 2
        d.text(SHAFT_LEFT - 30, label_y, str(floor), color="black", size=14)

    # Bold outlines:
    # outer shaft border + floor dividers
    shaft_bottom = floor_top(1) + FLOOR_HEIGHT

    # outer rectangle (4 sides)
    d.line(SHAFT_LEFT - 1, SHAFT_TOP, SHAFT_RIGHT + 1, SHAFT_TOP,
           color="black", width=BORDER)
    d.line(SHAFT_LEFT - 1, shaft_bottom, SHAFT_RIGHT + 1, shaft_bottom,
           color="black", width=BORDER)
    d.line(SHAFT_LEFT, SHAFT_TOP, SHAFT_LEFT, shaft_bottom,
           color="black", width=BORDER)
    d.line(SHAFT_RIGHT, SHAFT_TOP, SHAFT_RIGHT, shaft_bottom,
           color="black", width=BORDER)

    # horizontal dividers between floors
    # (floor_top(1) through floor_top(5))
    for floor in range(1, FLOOR_COUNT):
        y = floor_top(floor)
        d.line(SHAFT_LEFT - 1, y, SHAFT_RIGHT + 1, y,
               color="black", width=BORDER)

    # --- elevator car at floor 1 (yellow fill + bold outline) ---
    margin = 20
    car_top = floor_top(1) + 10
    car_bottom = floor_top(1) + FLOOR_HEIGHT
    car_left = SHAFT_LEFT + margin
    car_right = SHAFT_RIGHT - margin
    d.rectangle(car_left, car_top, car_right, car_bottom,
                color="yellow", outline=False)
    d.line(car_left, car_top, car_right, car_top,
           color="black", width=BORDER)
    d.line(car_left, car_bottom, car_right, car_bottom,
           color="black", width=BORDER)
    d.line(car_left, car_top, car_left, car_bottom,
           color="black", width=BORDER)
    d.line(car_right, car_top, car_right, car_bottom,
           color="black", width=BORDER)

    app.display()


if __name__ == "__main__":
    main()
