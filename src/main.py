from utils import args
import time
import io
from Matrix import Matrix
from datetime import date
from datetime import timedelta
import requests
import datetime

def center_text(text, matrix_width=64, char_width=4, char_spacing=1):
    text_width = len(text) * char_width + (len(text) - 1) * char_spacing
    x_position = (matrix_width - text_width) // 2
    return x_position

if __name__ == "__main__":
    cliArgs = args()

    matrix_width = 64
    matrix_height = 64
    matrix = Matrix(matrix_width, matrix_height,
                    brightness=cliArgs.led_brightness, debug=cliArgs.debug)



    # Split
    workout_split = [ "Chest/Abs", "Back", "Legs", "Arms", "Rest" ]
    workout_split_seed = 1

    # Start date: October 2, 2025
    start_date = datetime.datetime(2025, 10, 2, 0, 0, 0)


    while True:
        try:
            current_time = datetime.datetime.now()
            elapsed = current_time - start_date
            
            total_seconds = int(elapsed.total_seconds())
            day = (elapsed.days) + 1
            week = (day // 7) + 1
            month = (day // 30) + 1
            
            time_str = current_time.strftime('%I:%M:%S %p')

            # Display
            matrix.drawText(f"Day {day}", "medium", (center_text(f"Day {day}"), 10), (178, 34, 52))
            matrix.drawText(f"Week {week}", "medium", (center_text(f"Week {week}"), 20), (255, 255, 255))
            matrix.drawText(f"Month {month}", "medium", (center_text(f"Month {month}"), 30), (60, 59, 110))
            matrix.drawText(f"{workout_split[(day + workout_split_seed) % len(workout_split)]}", "medium", (center_text(workout_split[(day + workout_split_seed) % len(workout_split)]), 50), (255, 255, 255))
            matrix.drawText(f"{time_str}", "medium", (center_text(time_str), 60), (160, 160, 160))
            
        except Exception as e:
            print(f"Exception: {e}")

        matrix.debugShow()
        
        time.sleep(1)  # Update every second
        matrix.clear()