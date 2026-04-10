"""
Elevator shaft with floor-button panel.
Press a floor button to send the cab there; the button clears on arrival.
After stopping at a floor, the elevator waits for 2 seconds,
then proceeds to the next call or returns to the first floor if no more calls.
"""

from guizero import App, Box, Drawing, PushButton

# Shaft geometry (within the Drawing widget)
SHAFT_LEFT = 80
SHAFT_RIGHT = 330
SHAFT_TOP = 50
FLOOR_COUNT = 6
FLOOR_HEIGHT = 83

BORDER = 2
ANIM_STEPS = 20  # frames per floor of travel
ANIM_DELAY = 20  # ms per frame

GREY = (200, 200, 200)


def floor_top(floor):
    """
    y-coordinate of the top edge of the given floor
    (1=bottom, 6=top)
    """
    return SHAFT_TOP + (FLOOR_COUNT - floor) * FLOOR_HEIGHT


def main():
    buttons: dict = {}  # floor number -> PushButton widget
    current_floor: int = 1
    animating: bool = False
    queue: list = []

    def draw_scene(car_y_top):
        """ Draw the scene with the cab in the correct location """
        d.clear()

        # Floor rectangles (brown fill) and numeric labels
        for _floor in range(1, FLOOR_COUNT + 1):
            y = floor_top(_floor)
            d.rectangle(SHAFT_LEFT, y, SHAFT_RIGHT, y + FLOOR_HEIGHT,
                        color="brown", outline=False)
            label_y = y + FLOOR_HEIGHT // 2
            d.text(SHAFT_LEFT - 40, label_y, str(_floor),
                   color="black", bold=True)

        shaft_bottom = floor_top(1) + FLOOR_HEIGHT

        # Outer shaft border
        d.line(SHAFT_LEFT - 1, SHAFT_TOP, SHAFT_RIGHT + 1, SHAFT_TOP,
               color="black", width=BORDER)
        d.line(SHAFT_LEFT - 1, shaft_bottom, SHAFT_RIGHT + 1, shaft_bottom,
               color="black", width=BORDER)
        d.line(SHAFT_LEFT, SHAFT_TOP, SHAFT_LEFT, shaft_bottom,
               color="black", width=BORDER)
        d.line(SHAFT_RIGHT, SHAFT_TOP, SHAFT_RIGHT, shaft_bottom,
               color="black", width=BORDER)

        # Horizontal floor dividers
        for _floor in range(1, FLOOR_COUNT):
            y = floor_top(_floor)
            d.line(SHAFT_LEFT - 1, y, SHAFT_RIGHT + 1, y,
                   color="black", width=BORDER)

        # Elevator cab (yellow rectangle with black outline)
        side_margin = 20
        top_margin = 10
        car_left = SHAFT_LEFT + side_margin
        car_right = SHAFT_RIGHT - side_margin
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

    def animate_step(start_y, end_y, step, total_steps, target_floor):
        """ Animate the steps to arrive at a floor """
        t = step / total_steps
        current_y = int(start_y + (end_y - start_y) * t)
        draw_scene(current_y)
        if step < total_steps:
            app.after(ANIM_DELAY,
                      lambda: animate_step(start_y, end_y, step + 1,
                                           total_steps, target_floor))
        else:
            # Arrived at destination
            nonlocal current_floor, animating
            current_floor = target_floor
            animating = False
            buttons[target_floor].bg = GREY  # clear the floor indicator
            app.after(2000, process_queue)  # wait before moving again

    def process_queue():
        nonlocal animating
        if animating:
            return

        if not queue:
            if current_floor != 1:
                queue.append(1)
            else:
                return

        target = queue.pop(0)
        if target == current_floor:
            buttons[target].bg = None  # already here — just clear it
            process_queue()
            return

        animating = True
        start_y = floor_top(current_floor) + 10
        end_y = floor_top(target) + 10
        total_steps = abs(target - current_floor) * ANIM_STEPS
        animate_step(start_y, end_y, 1, total_steps, target)

    def floor_button_pressed(_floor):
        """
        Light the button and queue the floor request
        when a floor button is pressed
        """
        if _floor not in queue and _floor != current_floor:
            queue.append(_floor)
            buttons[_floor].bg = "yellow"
        process_queue()

    # UI layout
    app = App(title="Elevator", width=530, height=640, bg="white")
    app.text_size = 14
    app.text_bold = True

    # Shaft drawing (left side)
    d = Drawing(app, width=370, height=580, align="left")

    # Floor-button panel (right side)
    button_box = Box(app, width=140, height=510, border=True, align="left")
    Box(button_box, width=10, height=28, border=False)  # spacer

    for floor in range(FLOOR_COUNT, 0, -1):
        btn = PushButton(button_box, text=str(floor),
                         command=floor_button_pressed, args=[floor])
        btn.bg = GREY

        buttons[floor] = btn
        Box(button_box, width=10, height=20, border=False)  # spacer

    draw_scene(floor_top(1) + 10)  # initial position: floor 1

    app.display()


if __name__ == "__main__":
    main()
