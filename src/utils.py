import argparse
from datetime import date


def args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--led-brightness", action="store", help="Brightness level 1-100 (default 100)", default=100,
                        type=int)
    parser.add_argument("--debug", action='store_true', help="Display image rather than writing to LED board")
    parser.add_argument("--start-date", action="store", help="Day 1 of the course, YYYY-MM-DD (default 2026-10-30)",
                        default=date(2026, 10, 30), type=date.fromisoformat)
    parser.add_argument("--days-per-lesson", action="store", help="Days between new lessons (default 2)", default=2,
                        type=float)
    parser.add_argument("--think", action="store", help="Seconds to recall before the answer shows (default 5)",
                        default=5, type=float)
    parser.add_argument("--answer", action="store", help="Seconds the answer stays up (default 4)", default=4,
                        type=float)

    return parser.parse_args()
