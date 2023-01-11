from PIL import Image
import time
import sys


PATH = "../assets/loading.png"

class Loading(object):
    def __init__(self, matrix):
        self.matrix = matrix
        self.image = Image.open(PATH)

    def render(self):
        self.matrix.SetImage(self.image.convert('RGB'))

    try:
        print("Press CTRL-C to stop.")
        while True:
            time.sleep(100)
    except KeyboardInterrupt:
        sys.exit(0)
