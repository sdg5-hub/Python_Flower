import math
import random
import tkinter as tk

WIDTH, HEIGHT = 900, 700
BG = "#101417"
CX, CY = 510, 390

root = tk.Tk()
root.title("Glass Flower")
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg=BG, highlightthickness=0)
canvas.pack()

rng = random.Random(12)


def point_on_petal(angle, length, width, t, across, opening):
    """A curved, pointed petal viewed at an angle."""
    spread = angle + (1 - opening) * 0.65
    distance = length * t

    # Petal width grows from its base, then narrows at the tip.
    half_width = width * (math.sin(math.pi * t) ** 0.85)
    sideways = across * half_width

    # Curl the petal upward and slightly outward.
    curl = 34 * math.sin(math.pi * t) * (1 - opening / 2)
    x = CX + math.cos(spread) * distance - math.sin(spread) * sideways
    y = CY + math.sin(spread) * distance + math.cos(spread) * sideways
    y -= curl * t
    return x, y


def draw_petal(angle, length, width, opening, shade):
    # Many fine lines give the petals their glasslike texture.
    for i in range(55):
        across = -1 + 2 * i / 54
        coords = []
        for step in range(31):
            t = step / 30
            x, y = point_on_petal(angle, length, width, t, across, opening)
            coords.extend((x, y))

        color = shade if i % 6 else "#c2d9e6"
        canvas.create_line(
            coords, fill=color, width=1,
            smooth=True, splinesteps=12
        )

    # Bright rim.
    for side in (-1, 1):
        coords = []
        for step in range(36):
            t = step / 35
            coords.extend(point_on_petal(
                angle, length, width, t, side, opening
            ))
        canvas.create_line(
            coords, fill="#a9c8d8", width=2,
            smooth=True, splinesteps=12
        )


def draw_stem():
    for offset, color in [
        (-3, "#56636d"), (0, "#b3bbc1"), (2, "#53636e")
    ]:
        canvas.create_line(
            CX + 33 + offset, CY + 19,
            CX + 85 + offset, HEIGHT + 20,
            fill=color, width=2, smooth=True
        )


def draw_stamens(opening):
    for i in range(25):
        angle = -math.pi + i * math.pi / 24
        length = rng.uniform(85, 145) * (0.45 + opening * 0.55)
        tip_x = CX + math.cos(angle) * length * 0.75
        tip_y = CY - 20 - abs(math.sin(angle)) * length

        canvas.create_line(
            CX + rng.uniform(-10, 10), CY + 6,
            tip_x, tip_y,
            fill="#829ba8", width=1, smooth=True
        )

        r = rng.uniform(4, 9)
        canvas.create_oval(
            tip_x - r, tip_y - r,
            tip_x + r, tip_y + r,
            outline="#b6cbd0", fill="#8ba5a6"
        )
        canvas.create_oval(
            tip_x - 2, tip_y - 3,
            tip_x + 1, tip_y,
            fill="#e1eee8", outline=""
        )


def draw_flower(frame=0):
    canvas.delete("all")
    opening = min(1.0, frame / 75)

    draw_stem()

    # Back petals first, front petals last.
    petals = [
        (-2.65, 205, 48, "#5c778a"),
        (-1.98, 235, 55, "#7190a3"),
        (-1.34, 210, 58, "#829cac"),
        (-0.68, 225, 47, "#607b8d"),
        (-0.18, 180, 44, "#647e91"),
        ( 3.03, 235, 58, "#7897ab"),
        ( 2.55, 215, 49, "#8da9b8"),
        ( 1.95, 195, 52, "#668398"),
        ( 1.30, 195, 55, "#9ab5c4"),
        ( 0.55, 190, 45, "#7593a5"),
    ]

    for angle, length, width, shade in petals[:5]:
        draw_petal(
            angle, length * (0.42 + 0.58 * opening),
            width * (0.5 + 0.5 * opening), opening, shade
        )

    if opening > 0.4:
        draw_stamens((opening - 0.4) / 0.6)

    for angle, length, width, shade in petals[5:]:
        draw_petal(
            angle, length * (0.42 + 0.58 * opening),
            width * (0.5 + 0.5 * opening), opening, shade
        )

    # Small iridescent details at the center.
    if opening > 0.5:
        for _ in range(35):
            x = CX + rng.uniform(-26, 26)
            y = CY + rng.uniform(-18, 18)
            color = rng.choice(
                ["#9bc9ce", "#c3a0b7", "#a3b596", "#d2dce0"]
            )
            canvas.create_oval(x, y, x + 2, y + 2, fill=color, outline="")

    if frame < 75:
        root.after(35, draw_flower, frame + 1)


draw_flower()
root.mainloop()