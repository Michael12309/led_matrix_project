import io
import os
from PIL import Image, ImageDraw, ImageFont

_PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_FONTS_DIR = os.path.join(_PROJECT_DIR, 'assets', 'fonts')

# Klee One looks like neat handwriting, so kana appear the way they're written
# (e.g. き and さ keep the gap in their lower stroke, unlike most printed fonts)
KANA_FONT = "KleeOne-SemiBold-hiragana.ttf"
KANA_SIZE = 44
# Kana are drawn 4x larger and shrunk down, with a quarter-pixel outline so the
# thin pen strokes stand out on the LEDs without filling in loops like ね and ぱ
# (half a pixel for small kana, whose strokes would otherwise be faint)
SUPERSAMPLE = 4
EMBOLDEN = 1
EMBOLDEN_SMALL = 2
SMALL_SIZE = 28
# Gap between kana in a word, as a fraction of the font size
KANA_GAP = 0.1

WHITE = (255, 240, 225)
GOLD = (255, 190, 50)
BLUE = (90, 180, 255)
GRAY = (150, 150, 170)
GREEN = (60, 190, 90)
DIM = (35, 35, 45)
TIMER = (40, 80, 150)

SCROLL_SPEED = 20  # pixels per second, for hints too long to fit
SCROLL_PAUSE = 1.0  # seconds to hold the start and the end of a scrolling hint
HINT_Y = 56


def ink_extent(font, text):
    """Left and right edge of the pixels drawn for text with a bitmap font."""
    box = font.getmask(text).getbbox()
    return (box[0], box[2]) if box else (0, 0)


class CardRenderer(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height

        # Read everything in now: rgbmatrix drops root privileges once it starts
        with open(os.path.join(_FONTS_DIR, KANA_FONT), "rb") as f:
            self.kana_font_data = f.read()
        self.font_large = ImageFont.load(os.path.join(_FONTS_DIR, "9x15B.pil"))
        self.font_medium = ImageFont.load(os.path.join(_FONTS_DIR, "7x13B.pil"))
        self.font_small = ImageFont.load(os.path.join(_FONTS_DIR, "5x7.pil"))
        self.font_tiny = ImageFont.load(os.path.join(_FONTS_DIR, "4x6.pil"))

        self.kana_fonts = {}
        self.kana_masks = {}

    def duration(self, card):
        """Seconds to show a card, long enough for its hint to scroll past once."""
        return card.think + max(card.answer, self.scroll_time(card.hint))

    def render(self, card, t):
        """Frame for `t` seconds into the card."""
        frame = Image.new("RGB", (self.width, self.height))
        draw = ImageDraw.Draw(frame)
        if card.kind == "progress":
            self.draw_progress(draw, card.progress)
            return frame

        answered = t >= card.think
        if card.kind == "kana":
            self.draw_kana_card(frame, draw, card, answered)
        elif card.kind == "pair":
            self.draw_pair_card(frame, draw, card, answered)
        elif card.kind == "word":
            self.draw_word_card(frame, draw, card, answered)

        if not answered:
            self.draw_timer(draw, t / card.think)
        elif card.hint:
            self.draw_scrolling(draw, card.hint, HINT_Y, GRAY, t - card.think)
        return frame

    def draw_kana_card(self, frame, draw, card, answered):
        kana = card.kana[0]
        mask = self.kana_mask(kana.char, self.fit_size(kana.char, self.width - 2, 41))
        self.paste_centered(frame, mask, (0, 0, self.width, 41), GOLD if card.new else WHITE)
        if answered:
            self.draw_centered(draw, kana.romaji, self.font_large, 0, self.width, 41, BLUE)

    def draw_pair_card(self, frame, draw, card, answered):
        half = self.width // 2
        size = min(self.fit_size(k.char, half - 6, 34) for k in card.kana)
        for i, kana in enumerate(card.kana):
            self.paste_centered(frame, self.kana_mask(kana.char, size), (i * half, 0, half, 36), WHITE)
            if answered:
                self.draw_centered(draw, kana.romaji, self.font_large, i * half, half, 37, BLUE)
        draw.line([(half - 1, 4), (half - 1, 50)], fill=DIM)

    def draw_word_card(self, frame, draw, card, answered):
        word, romaji = card.word
        mask = self.kana_mask(word, self.fit_size(word, self.width - 2, 32, 40))
        self.paste_centered(frame, mask, (0, 0, self.width, 35), WHITE)
        if answered:
            left, right = ink_extent(self.font_large, romaji)
            font = self.font_large if right - left <= self.width - 2 else self.font_medium
            self.draw_centered(draw, romaji, font, 0, self.width, 37, BLUE)

    def draw_progress(self, draw, progress):
        self.draw_centered(draw, f"DAY {progress.day}", self.font_large, 0, self.width, 1, WHITE)

        # One segment per lesson: learned, newest, still locked
        segment = self.width // progress.lessons
        x = (self.width - segment * progress.lessons) // 2
        for i in range(progress.lessons):
            color = GREEN if i < progress.lesson - 1 else GOLD if i == progress.lesson - 1 else DIM
            draw.rectangle([x, 19, x + segment - 2, 21], fill=color)
            x += segment

        known = f"{progress.known}/{progress.total} kana"
        self.draw_centered(draw, known, self.font_small, 0, self.width, 25, GRAY)

        self.draw_centered(draw, "new:", self.font_tiny, 0, self.width, 35, GOLD)
        romaji = [kana.romaji for kana in progress.newest]
        per_line = len(romaji)
        while ink_extent(self.font_tiny, " ".join(romaji[:per_line]))[1] > self.width - 2:
            per_line -= 1
        lines = -(-len(romaji) // per_line)
        per_line = -(-len(romaji) // lines)  # even out the lines, e.g. 3 + 3 rather than 4 + 2
        for i in range(lines):
            line = " ".join(romaji[i * per_line:(i + 1) * per_line])
            self.draw_centered(draw, line, self.font_tiny, 0, self.width, 42 + i * 7, GOLD)

        if progress.next_in is None:
            footer = "all unlocked!"
        else:
            hours = int(progress.next_in.total_seconds() // 3600)
            minutes = int(progress.next_in.total_seconds() % 3600 // 60)
            footer = f"next in {hours // 24}d {hours % 24}h" if hours >= 24 else f"next in {hours}h {minutes}m"
        self.draw_centered(draw, footer, self.font_tiny, 0, self.width, 57, GRAY)

    def draw_timer(self, draw, fraction):
        """Bar along the bottom that shrinks towards the middle until the answer shows."""
        half = round(self.width / 2 * (1 - fraction))
        if half > 0:
            draw.rectangle([self.width // 2 - half, self.height - 2, self.width // 2 + half - 1, self.height - 1],
                           fill=TIMER)

    def scroll_time(self, text):
        if not text:
            return 0
        left, right = ink_extent(self.font_small, text)
        overflow = right - left - (self.width - 2)
        return overflow / SCROLL_SPEED + 2 * SCROLL_PAUSE if overflow > 0 else 0

    def draw_scrolling(self, draw, text, y, color, t):
        """Centered if it fits, otherwise hold the start, scroll to the end, and hold."""
        left, right = ink_extent(self.font_small, text)
        overflow = right - left - (self.width - 2)
        if overflow <= 0:
            self.draw_centered(draw, text, self.font_small, 0, self.width, y, color)
            return
        offset = min(overflow, max(0.0, t - SCROLL_PAUSE) * SCROLL_SPEED)
        draw.text((1 - left - round(offset), y), text, font=self.font_small, fill=color)

    def draw_centered(self, draw, text, font, x, width, y, color):
        left, right = ink_extent(font, text)
        draw.text((x + (width - (right - left)) // 2 - left, y), text, font=font, fill=color)

    def paste_centered(self, frame, mask, box, color):
        x, y, width, height = box
        frame.paste(color, (x + (width - mask.width) // 2, y + (height - mask.height) // 2), mask)

    def fit_size(self, text, max_width, max_height, size=KANA_SIZE):
        """Largest font size up to `size` at which the kana fit in the given box."""
        mask = self.kana_mask(text, size)
        while mask.width > max_width or mask.height > max_height:
            size = min(size - 1, int(size * min(max_width / mask.width, max_height / mask.height)))
            mask = self.kana_mask(text, size)
        return size

    def kana_mask(self, text, size):
        """Anti-aliased mask of the kana, cropped to the pixels they cover."""
        key = (text, size)
        if key not in self.kana_masks:
            if size not in self.kana_fonts:
                self.kana_fonts[size] = ImageFont.truetype(io.BytesIO(self.kana_font_data), size * SUPERSAMPLE,
                                                           layout_engine=ImageFont.Layout.BASIC)
            font = self.kana_fonts[size]
            stroke = EMBOLDEN_SMALL if size < SMALL_SIZE else EMBOLDEN

            # Space kana by the pixels they cover rather than the font's square cells,
            # so small ゃゅょ sit snug against the kana before them and words fit larger
            pieces = []
            for char in text:
                left, top, right, bottom = font.getbbox(char, stroke_width=stroke)
                pad = 2 * stroke
                glyph = Image.new("L", (right - left + 2 * pad, bottom - top + 2 * pad), 0)
                ImageDraw.Draw(glyph).text((pad - left, pad - top), char, font=font, fill=255,
                                           stroke_width=stroke, stroke_fill=255)
                ink = glyph.getbbox()
                # Keep each kana's height above the baseline, e.g. small kana sit low
                pieces.append((glyph.crop(ink), top - pad + ink[1]))
            gap = round(size * SUPERSAMPLE * KANA_GAP)
            width = sum(glyph.width for glyph, _ in pieces) + gap * (len(pieces) - 1)
            top = min(y for _, y in pieces)
            height = max(y + glyph.height for glyph, y in pieces) - top

            # Pad to whole output pixels so shrinking doesn't smear the edges
            big = Image.new("L", (width // SUPERSAMPLE * SUPERSAMPLE + 2 * SUPERSAMPLE,
                                  height // SUPERSAMPLE * SUPERSAMPLE + 2 * SUPERSAMPLE), 0)
            x = SUPERSAMPLE
            for glyph, y in pieces:
                big.paste(glyph, (x, SUPERSAMPLE + y - top))
                x += glyph.width + gap
            mask = big.reduce(SUPERSAMPLE)
            self.kana_masks[key] = mask.crop(mask.getbbox())
        return self.kana_masks[key]
