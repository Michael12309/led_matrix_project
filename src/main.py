from utils import args
import time
from datetime import datetime
from Matrix import Matrix
from cards import CardRenderer
from scheduler import Scheduler

FPS = 20

if __name__ == "__main__":
    cliArgs = args()

    matrix_width = 64
    matrix_height = 64

    # Load fonts before Matrix init (rgbmatrix drops root privileges to UID 1)
    renderer = CardRenderer(matrix_width, matrix_height)
    start_date = datetime.combine(cliArgs.start_date, datetime.min.time())
    scheduler = Scheduler(start_date, cliArgs.days_per_lesson, cliArgs.think, cliArgs.answer)

    matrix = Matrix(matrix_width, matrix_height,
                    brightness=cliArgs.led_brightness, debug=cliArgs.debug)

    try:
        while True:
            try:
                card = scheduler.next_card(datetime.now())
                duration = renderer.duration(card)
                start = time.monotonic()
                t = 0
                while t < duration:
                    matrix.show(renderer.render(card, t))
                    time.sleep(1 / FPS)
                    t = time.monotonic() - start
            except Exception as e:
                print(f"Exception: {e}")
                time.sleep(1)
    except KeyboardInterrupt:
        matrix.clear()
