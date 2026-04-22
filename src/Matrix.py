from PIL import Image, ImageFont, ImageDraw

class Matrix(object):
    def __init__(self, width, height, brightness=100, debug=False):
        self.debug = debug
        self.width = width
        self.height = height

        if not self.debug:
            from rgbmatrix import RGBMatrix, RGBMatrixOptions
            from rgbmatrix import graphics
            
            # Configuration for the matrix
            options = RGBMatrixOptions()
            options.rows = self.height
            options.cols = self.width
            options.chain_length = 1
            options.parallel = 1
            options.brightness = brightness # cliArgs.led_brightness
            options.hardware_mapping = 'adafruit-hat'  # necessary if using Adafruit HAT (I am)

            self.matrix = RGBMatrix(options=options)
        
            self.font_medium = graphics.Font()
            self.font_medium.LoadFont("../assets/fonts/5x7.bdf")

            self.font_small = graphics.Font()
            self.font_small.LoadFont("../assets/fonts/4x6.bdf")
        else:
            self.led_board = Image.new(mode='RGB', size=(self.width, self.height), color=(0,0,0))
            self.draw = ImageDraw.Draw(self.led_board)
            self.debug_font_medium = ImageFont.load("../assets/fonts/5x7.pil")
            self.debug_font_small = ImageFont.load("../assets/fonts/4x6.pil")

    def drawImage(self, img, pos):
        if not self.debug:
            self.matrix.SetImage(img.convert('RGB'), pos[0], pos[1])
        else:
            if img.mode == 'RGBA':
                self.led_board.paste(img, pos, img)
            else:
                self.led_board.paste(img, pos)
            
    def drawText(self, text, font_size, pos, color):
        if not self.debug:
            # TODO: improve, this is slow
            from rgbmatrix import graphics
            font = self.font_small if font_size == 'small' else self.font_medium
            graphics.DrawText(self.matrix, font, pos[0], pos[1], graphics.Color(color[0], color[1], color[2]), text)
        else:
            font = font = self.debug_font_small if font_size == 'small' else self.debug_font_medium
            adjust_height = -5 if font_size == 'small' else -6
            self.draw.text((pos[0], pos[1] + adjust_height), text, fill=(color[0], color[1], color[2]), font=font)

    def drawHLine(self, y, x_start, x_end, color):
        if not self.debug:
            from rgbmatrix import graphics
            graphics.DrawLine(self.matrix, x_start, y, x_end, y, graphics.Color(color[0], color[1], color[2]))
        else:
            self.draw.line([(x_start, y), (x_end, y)], fill=(color[0], color[1], color[2]))

    def drawRect(self, x, y, width, height, color):
        if not self.debug:
            from rgbmatrix import graphics
            c = graphics.Color(color[0], color[1], color[2])
            for row in range(y, y + height):
                graphics.DrawLine(self.matrix, x, row, x + width - 1, row, c)
        else:
            self.draw.rectangle(
                [(x, y), (x + width - 1, y + height - 1)],
                fill=(color[0], color[1], color[2])
            )

    def drawRectOutline(self, x, y, width, height, color):
        if not self.debug:
            from rgbmatrix import graphics
            c = graphics.Color(color[0], color[1], color[2])
            graphics.DrawLine(self.matrix, x, y, x + width - 1, y, c)
            graphics.DrawLine(self.matrix, x, y + height - 1, x + width - 1, y + height - 1, c)
            graphics.DrawLine(self.matrix, x, y, x, y + height - 1, c)
            graphics.DrawLine(self.matrix, x + width - 1, y, x + width - 1, y + height - 1, c)
        else:
            self.draw.rectangle(
                [(x, y), (x + width - 1, y + height - 1)],
                outline=(color[0], color[1], color[2]),
                fill=None
            )

    def drawPixel(self, x, y, color):
        if not self.debug:
            self.matrix.SetPixel(x, y, color[0], color[1], color[2])
        else:
            self.draw.point((x, y), fill=(color[0], color[1], color[2]))

    def drawSprite(self, sprite_data, x_offset, y_offset):
        for row_idx, row in enumerate(sprite_data):
            for col_idx, pixel in enumerate(row):
                if pixel is not None:
                    self.drawPixel(x_offset + col_idx, y_offset + row_idx, pixel)

    def clear(self):
        if not self.debug:
            self.matrix.Clear()
        else:
            self.draw.rectangle([(0,0), (self.width, self.height)], fill=(0,0,0))

    def debugShow(self):
        if self.debug:
            large = self.led_board.resize((self.width*15, self.height*15), Image.Resampling.NEAREST)
            large.show()
