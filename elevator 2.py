"""
Elevator shaft and elevator cab drawing
"""

from guizero import App, Box, Drawing, PushButton

# Elevator Shaft Geometry
SHAFT_LEFT = 150
SHAFT_RIGHT = 350
SHAFT_TOP = 50
FLOOR_COUNT = 6
FLOOR_HEIGHT = 83
SHAFT_BOTTOM = SHAFT_TOP + FLOOR_COUNT * FLOOR_HEIGHT

BORDER = 2  # outline width in pixels

ANIM_STEPS = 30
ANIM_DELAY = 10  # ms per frame


def floor_top(floor):
    """ Return the y coordinate of the top edge of the given floor
     (1=bottom, 6=top) """
    return SHAFT_TOP + (FLOOR_COUNT - floor) * FLOOR_HEIGHT


def main():
    def draw_scene(car_y_top):
        d.clear()

        # --- floor rectangles (brown fill, no outline) and labels ---
        for floor in range(1, FLOOR_COUNT + 1):
            y = floor_top(floor)
            d.rectangle(SHAFT_LEFT, y, SHAFT_RIGHT, y + FLOOR_HEIGHT,
                        color="brown", outline=False)
            label_y = y + FLOOR_HEIGHT // 2
            d.text(SHAFT_LEFT - 30, label_y, str(floor),
                   color="black", bold=True)

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
        for floor in range(1, FLOOR_COUNT):
            y = floor_top(floor)
            d.line(SHAFT_LEFT - 1, y, SHAFT_RIGHT + 1, y,
                   color="black", width=BORDER)

        # --- elevator car (yellow fill + bold outline) ---
        side_margin = 20
        car_left = SHAFT_LEFT + side_margin
        car_right = SHAFT_RIGHT - side_margin

        top_margin = 10
        car_bottom = car_y_top + FLOOR_HEIGHT - top_margin

        d.rectangle(car_left, car_y_top, car_right, car_bottom,
                    color="yellow", outline=False)
        d.line(car_left, car_y_top, car_right, car_y_top,
               color="black", width=BORDER)
        d.line(car_left, car_bottom, car_right, car_bottom,
               color="black", width=BORDER)
        d.line(car_left, car_y_top, car_left, car_bottom,
               color="black", width=BORDER)
        d.line(car_right, car_y_top, car_right, car_bottom,
               color="black", width=BORDER)

    def animate_step(start_y, end_y, step):
        """ Event handler to animate cab motion """
        t = step / ANIM_STEPS
        current_y = int(start_y + (end_y - start_y) * t)
        draw_scene(current_y)
        if step < ANIM_STEPS:
            app.after(ANIM_DELAY,
                      lambda: animate_step(start_y, end_y, step + 1))
        else:
            state["animating"] = False

    def go_up():
        """ Event handler to go up one floor """
        if state["animating"] or state["floor"] >= FLOOR_COUNT:
            return
        state["animating"] = True
        start_floor = state["floor"]
        state["floor"] += 1
        start_y = floor_top(start_floor) + 10
        end_y = floor_top(state["floor"]) + 10
        animate_step(start_y, end_y, 1)

    def go_down():
        """ Event handler to go down one floor """
        if state["animating"] or state["floor"] <= 1:
            return
        state["animating"] = True
        start_floor = state["floor"]
        state["floor"] -= 1
        start_y = floor_top(start_floor) + 10
        end_y = floor_top(state["floor"]) + 10
        animate_step(start_y, end_y, 1)

    app = App(title="Elevator Shaft and Cab",
              width=450, height=650, bg="white")
    app.text_size = 14
    app.text_bold = True

    d = Drawing(app, width=450, height=550)

    state = {"floor": 1, "animating": False}

    # Initial draw
    draw_scene(floor_top(1) + 10)

    # UP/DOWN buttons at the bottom of the screen
    Box(app, height=20, width=20, align="bottom")  # Spacer
    button_box = Box(app, height=50, width=300,
                     align="bottom", border=False)

    PushButton(button_box, text="Up", width=10, height=2,
               align="left", command=go_up)
    PushButton(button_box, text="Down", width=10, height=2,
               align="right", command=go_down)

    app.display()


if __name__ == "__main__":
    main()
