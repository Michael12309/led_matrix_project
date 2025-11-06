from utils import args
import time
import io
from Matrix import Matrix
from datetime import date
from datetime import timedelta
import requests
import datetime

if __name__ == "__main__":
    cliArgs = args()

    matrix_width = 64
    matrix_height = 64
    matrix = Matrix(matrix_width, matrix_height,
                    brightness=cliArgs.led_brightness, debug=cliArgs.debug)

    # Start date: October 2, 2025
    start_date = datetime.datetime(2025, 10, 2, 0, 0, 0)


    while True:
        try:
            current_time = datetime.datetime.now()
            elapsed = current_time - start_date
            
            total_seconds = int(elapsed.total_seconds())
            days = elapsed.days
            weeks = days // 7
            months = days // 30
            
            # Display
            matrix.drawText(f"Day {days}", "medium", (1, 7), (100, 245, 129))
            matrix.drawText(f"Week {weeks}", "medium", (1, 20), (100, 245, 129))
            matrix.drawText(f"Month {months}", "medium", (1, 33), (198, 174, 245))
            matrix.drawText(f"Second {total_seconds}", "medium", (1, 46), (216, 245, 100))
            
        except Exception as e:
            print(f"Exception: {e}")

        matrix.debugShow()
        
        time.sleep(1)  # Update every second
        matrix.clear()
