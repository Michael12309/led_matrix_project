from utils import args
import time
from PIL import Image
import io
import PIL
import matplotlib.pyplot as plt
import yfinance as yf
from Matrix import Matrix
from datetime import date
import pandas as pd

if __name__ == "__main__":
    cliArgs = args()

    matrix_width = 64
    matrix_height = 32
    matrix = Matrix(brightness=cliArgs.led_brightness, debug=cliArgs.debug)

    color_green = (69, 221, 110)
    color_green_inverted = (186, 34, 145)

    color_red = (221, 69, 69)
    color_red_inverted = (34, 186, 186)

    ticker = 'TRST'

    while True:
        data = yf.download(tickers=ticker, period='5d', interval='1m', prepost=True)
        
        x = 0 # wrong datatype but it works
        y = 0 # ^
        previous_close = 0
        starting_price = 0
        last_price = 0
        first_open = 0
        try:
            print(data)
            today_data = data[data.index.normalize() == pd.Timestamp(date.today(), tz=data.index.tz)]
            previous_data = data[data.index < today_data.index[0]]
            previous_close = previous_data['Close'].iloc[-1]
            data = today_data
            
            x = data.index.to_series().to_numpy()
            y = data['Close'].to_numpy()
            
            starting_price = data['Open'].iloc[0]
            last_price = data['Close'].iloc[-1]
        except IndexError:
            print('Error: No data points, trying again in 5 seconds')
            time.sleep(5)
            continue

        # set plot window size, use lower numbers for lower resolution, 2:1 is ideal
        f = plt.figure()
        f.set_figwidth(15)
        # squash
        f.set_figheight(4)

        fill_color = (color_green_inverted[0] / 255, color_green_inverted[1] / 255, color_green_inverted[2] / 255) if last_price > starting_price else (color_red_inverted[0] / 255, color_red_inverted[1] / 255, color_red_inverted[2] / 255)
        plt.fill_between(x, y, starting_price, alpha=0.5, color=fill_color)
        plt.plot(x, y, color='black', linewidth=5)

        plt.xticks([])
        plt.yticks([])
        plt.axis('off')

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        im = Image.open(buf)
        width, height = im.size
        im = im.crop((width * .14, height * .1, width * .86, height * .9))
        im = im.convert('RGB')
        im = PIL.ImageOps.invert(im)

        im.thumbnail((matrix_width, matrix_height), Image.Resampling.LANCZOS)

        matrix.drawImage(im, (0, 14))

        matrix.drawText(ticker, "medium", (0, 7), (49, 50, 117))
        current_price = f'$ {round(last_price, 2):.2f}'
        current_change = round(last_price - previous_close, 2)
        current_change = f'+{current_change:.2f}' if current_change > 0 else f'{current_change:.2f}'

        matrix.drawText(current_price, "medium", (29, 7), (255, 255, 255))
        matrix.drawText(current_change, "small", (44, 13), (160, 160, 160))

        matrix.debugShow()

        # stock only updates once a minute, but we probably won't be on the exact minute
        time.sleep(60 / 4)
        buf.close()
        plt.close()
