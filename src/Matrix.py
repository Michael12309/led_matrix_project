import os
import time
from PIL import Image

_PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEBUG_SCALE = 10


class Matrix(object):
    def __init__(self, width, height, brightness=100, debug=False):
        self.debug = debug
        self.width = width
        self.height = height

        if not self.debug:
            from rgbmatrix import RGBMatrix, RGBMatrixOptions

            # Configuration for the matrix
            options = RGBMatrixOptions()
            options.rows = self.height
            options.cols = self.width
            options.chain_length = 1
            options.parallel = 1
            options.brightness = brightness # cliArgs.led_brightness
            options.hardware_mapping = 'adafruit-hat'  # necessary if using Adafruit HAT (I am)

            # This drops root privileges, so anything read from disk must be loaded first
            self.matrix = RGBMatrix(options=options)
            # Frames are drawn offscreen and swapped in, so they don't flicker
            self.canvas = self.matrix.CreateFrameCanvas()
        else:
            self.window = None
            self.closed = False
            try:
                import tkinter
                self.window = tkinter.Tk()
                self.window.title("LED Matrix")
                self.window.protocol("WM_DELETE_WINDOW", self.close)
                self.label = tkinter.Label(self.window, bg="black")
                self.label.pack()
            except Exception as e:  # e.g. no display over SSH
                self.debug_file = os.path.join(_PROJECT_DIR, "debug.png")
                self.last_saved = 0
                print(f"No debug window ({e}), saving frames to {self.debug_file}")

    def show(self, frame):
        """Display a full RGB frame the size of the matrix."""
        if not self.debug:
            self.canvas.SetImage(frame)
            self.canvas = self.matrix.SwapOnVSync(self.canvas)
            return

        large = frame.resize((self.width * DEBUG_SCALE, self.height * DEBUG_SCALE), Image.Resampling.NEAREST)
        if self.window:
            from PIL import ImageTk
            self.photo = ImageTk.PhotoImage(large)  # keep a reference, or Tk shows nothing
            self.label.configure(image=self.photo)
            self.window.update()
            # Exit from here: Tk swallows exceptions raised inside its own callbacks
            if self.closed:
                raise SystemExit
        elif time.monotonic() - self.last_saved > 0.5:
            large.save(self.debug_file)
            self.last_saved = time.monotonic()

    def clear(self):
        if not self.debug:
            self.matrix.Clear()

    def close(self):
        self.closed = True
