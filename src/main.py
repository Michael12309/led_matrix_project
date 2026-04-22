from utils import args
import time
from Matrix import Matrix
from datetime import date
import datetime
from PIL import Image
from donut_store import load_donuts
from uv_fetch import get_uv_index

def center_text(text, matrix_width=64, font_size="small"):
    char_width = 3 if font_size == "small" else 5
    char_spacing = 1
    text_width = len(text) * char_width + (len(text) - 1) * char_spacing
    return max((matrix_width - text_width) // 2, 0)

def center_text_in_half(text, half_start, half_width=32, font_size="small"):
    char_width = 3 if font_size == "small" else 5
    char_spacing = 1
    text_width = len(text) * char_width + (len(text) - 1) * char_spacing
    return half_start + max((half_width - text_width) // 2, 0)

def get_uv_color(uv):
    if uv <= 2:
        return (0, 180, 0)
    elif uv <= 5:
        return (220, 200, 0)
    elif uv <= 7:
        return (220, 130, 0)
    elif uv <= 10:
        return (220, 30, 30)
    else:
        return (180, 0, 220)

def draw_bar(matrix, x, y, width, height, count, max_count, fill_color, outline_color):
    matrix.drawRectOutline(x, y, width, height, outline_color)
    if count > 0:
        fill_height = round(count / max_count * (height - 2))
        fill_height = max(fill_height, 1)
        fill_y = y + height - 1 - fill_height
        matrix.drawRect(x + 1, fill_y, width - 2, fill_height, fill_color)

if __name__ == "__main__":
    cliArgs = args()

    matrix_width = 64
    matrix_height = 64
    matrix = Matrix(matrix_width, matrix_height,
                    brightness=cliArgs.led_brightness, debug=cliArgs.debug)

    # Workout config
    workout_split = ["Push", "Run/Mobility", "Pull", "Legs"]
    workout_split_seed = 2
    start_date = datetime.datetime(2025, 10, 2, 0, 0, 0)

    MAX_DONUTS = 10

    # Load donut image
    donut_img = Image.open("../assets/donut_14x14.png")

    while True:
        try:
            current_time = datetime.datetime.now()
            elapsed = current_time - start_date
            day = elapsed.days + 1

            workout = workout_split[(day + workout_split_seed) % len(workout_split)]
            time_str = current_time.strftime('%I:%M:%S %p')

            michael_owes, tyler_owes = load_donuts()
            michael_owes = min(michael_owes, MAX_DONUTS)
            tyler_owes = min(tyler_owes, MAX_DONUTS)

            uv = get_uv_index()

            # === Section 1: Donut Counter (rows 0-25) ===
            # Labels
            matrix.drawText("MICHAEL", "small",
                            (center_text_in_half("MICHAEL", 0), 7),
                            (220, 140, 40))
            matrix.drawText("TYLER", "small",
                            (center_text_in_half("TYLER", 32), 7),
                            (40, 140, 220))

            # Bar graphs (rows 9-23, 15px tall)
            draw_bar(matrix, 6, 9, 15, 15, michael_owes, MAX_DONUTS,
                     (220, 140, 40), (50, 50, 50))
            draw_bar(matrix, 43, 9, 15, 15, tyler_owes, MAX_DONUTS,
                     (40, 140, 220), (50, 50, 50))

            # Donut image centered between bars
            matrix.drawImage(donut_img, (25, 10))

            # Count numbers below bars
            m_str = str(michael_owes)
            t_str = str(tyler_owes)
            matrix.drawText(m_str, "small",
                            (center_text_in_half(m_str, 6, 15), 25),
                            (200, 200, 200))
            matrix.drawText(t_str, "small",
                            (center_text_in_half(t_str, 43, 15), 25),
                            (200, 200, 200))

            # === Separator ===
            matrix.drawHLine(26, 4, 59, (40, 40, 40))

            # === Section 2: UV Index (rows 27-36) ===
            uv_color = get_uv_color(uv)
            matrix.drawText("UV", "small", (2, 34), (160, 160, 160))
            matrix.drawText(str(uv), "medium", (14, 34), uv_color)
            # Color bar
            matrix.drawRect(2, 35, 60, 2, uv_color)

            # === Separator ===
            matrix.drawHLine(37, 4, 59, (40, 40, 40))

            # === Section 3: Workout (rows 38-50) ===
            day_str = f"Day {day}"
            matrix.drawText(day_str, "medium",
                            (center_text(day_str, font_size="medium"), 44),
                            (220, 220, 220))
            matrix.drawText(workout, "small",
                            (center_text(workout, font_size="small"), 50),
                            (180, 180, 180))

            # === Section 4: Time (rows 51-63) ===
            matrix.drawText(time_str, "medium",
                            (center_text(time_str, font_size="medium"), 59),
                            (80, 80, 80))

        except Exception as e:
            print(f"Exception: {e}")

        matrix.debugShow()

        time.sleep(1)
        matrix.clear()
