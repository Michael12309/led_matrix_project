# from loading import Loading
from utils import args
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
import time
import sys
from PIL import Image
import io
import PIL
import matplotlib.pyplot as plt
import yfinance as yf

if __name__ == "__main__":

    cliArgs = args()
    print(cliArgs)

    # Configuration for the matrix
    options = RGBMatrixOptions()
    options.rows = 32
    options.cols = 64
    options.chain_length = 1
    options.parallel = 1
    options.brightness = cliArgs.led_brightness # cliArgs.led_brightness
    options.hardware_mapping = 'adafruit-hat'  # necessary if using Adafruit HAT (I am)

    matrix = Matrix(RGBMatrix(options=options), debug=cliArgs.debug)

    #font = graphics.Font()
    #font.LoadFont("../assets/fonts/5x7.bdf")

    #font_small = graphics.Font()
    #font_small.LoadFont("../assets/fonts/4x6.bdf")

    color_green = (69, 221, 110)
    color_green_inverted = (186, 34, 145)

    color_red = (221, 69, 69)
    color_red_inverted = (34, 186, 186)

    ticker = 'TRST'

    while True:
        data = yf.download(tickers=ticker, period='1d', interval='1m')
        print(data)

        x = data.index.to_series().to_numpy()
        y = data['Adj Close'].to_numpy()

        starting_price = 0
        last_price = 0
        try:
            starting_price = data['Adj Close'][0]
            last_price = data['Adj Close'][-1]
        except IndexError:
            print('Error: No data points, trying again in 5 seconds')
            time.sleep(5)
            continue

        # set plot window size, use lower numbers for lower resolution, 2:1 is ideal
        f = plt.figure()
        f.set_figwidth(20)
        # squash
        f.set_figheight(3)

        fill_color = (color_green_inverted[0] / 255, color_green_inverted[1] / 255, color_green_inverted[2] / 255) if last_price > starting_price else (color_red_inverted[0] / 255, color_red_inverted[1] / 255, color_red_inverted[2] / 255)
        plt.fill_between(x, y, starting_price, alpha=0.5, color=fill_color)
        plt.plot(x, y, color='black', linewidth=3)

        plt.xticks([])
        plt.yticks([])
        plt.axis('off')

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        im = Image.open(buf)
        width, height = im.size
        im = im.crop((width * .13, height * .1, width * .87, height * .9))
        im = im.convert('RGB')
        im = PIL.ImageOps.invert(im)

        im.thumbnail((matrix.width, matrix.height - 10), Image.Resampling.LANCZOS)

        #matrix.Clear()
        #matrix.SetImage(im, 0, 20)

        graphics.DrawText(matrix, font, 0, 7, graphics.Color(49, 50, 117), ticker)
        current_price = '$ ' + str(round(last_price, 2))
        current_change = round(last_price - starting_price, 2)
        print('last', last_price, 'start', starting_price, 'minus', last_price - starting_price)
        current_change = '+' + str(current_change) if current_change > 0 else str(current_change)
        # change_color = graphics.Color(color_green[0], color_green[1], color_green[2]) if last_price > starting_price else graphics.Color(color_red[0], color_red[1], color_red[2])
        change_color = graphics.Color(160, 160, 160)
        graphics.DrawText(matrix, font, 29, 7, graphics.Color(255, 255, 255), current_price)
        graphics.DrawText(matrix, font_small, 44, 13, change_color, current_change)

        time.sleep(60)
        buf.close()
        plt.close()
