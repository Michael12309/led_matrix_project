import argparse


def args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--led-brightness", action="store", help="Brightness level 1-100 (default 100)", default=100,
                        type=int)
    parser.add_argument("--debug", action='store_true', help="Display image rather than writing to LED board")

    return parser.parse_args()
