# LED Matrix

This is made with a Raspberry Pi and a [Adafruit RGB LED Matrix](https://www.adafruit.com/product/2279).
It uses this submodule https://github.com/hzeller/rpi-rgb-led-matrix.git to simplify reading and writing to the LED matrix in CPython.

Result here:
![LED Matrix Final](https://github.com/Michael12309/led_matrix_project/assets/40968057/18b14a91-ef0a-4891-932d-4bc7f8140aa1)

# Hiragana flash cards

The board shows a hiragana character, gives you a few seconds to recall its sound (the blue bar along the
bottom counts down), then reveals the romaji underneath.

How it helps you memorize:

- **Active recall**: you try to remember before the answer appears, which builds memory far better than
  re-reading a chart.
- **Spaced repetition (Leitner system)**: a new lesson unlocks every 2 days, following the rows of the kana chart
  (あいうえお, かきくけこ, ...), then dakuten (が, ぱ, ...) and combinations (きゃ, しょ, ...): 104 kana in 21 lessons.
  A kana moves up a box 1, 3, 7, 14 and 30 days after its lesson unlocks, and each box comes up half as often as
  the one before, so new kana get drilled while old ones keep coming back at a slower pace. Familiar kana also get
  less time to think, pushing towards instant recognition.
- **Mnemonics**: for its first 3 days, a kana's answer comes with a shape-to-sound hint (き: "a KEY with two
  teeth"); dakuten and combinations show how they're built ("ki + small ya = kya").
- **Look-alikes**: easily confused kana (ぬ/め, は/ほ, る/ろ, ...) are shown side by side with a tip for telling
  them apart.
- **Real words**: everyday words spelled only with unlocked kana (ねこ cat, さくら cherry blossom) for reading
  practice.

Gold kana were unlocked today. At startup, whenever a lesson unlocks, and every few minutes, a progress screen
shows the day, the lessons unlocked and the newest kana.

Options (`python main.py --help`):

| Flag | Default | |
| --- | --- | --- |
| `--start-date` | 2026-10-30 | Day 1 of the course. Move it back 2 days per lesson to skip ones you know |
| `--days-per-lesson` | 2 | Days between new lessons |
| `--think` | 5 | Seconds to recall before the answer shows |
| `--answer` | 4 | Seconds the answer stays up |
| `--led-brightness` | 100 | Brightness level 1-100 |
| `--debug` | | Show the board in a window instead of on the LEDs (or save `debug.png` if there's no display) |

Kana are drawn with [Klee One](https://github.com/fontworks-fonts/Klee), a handwriting-style font, so they look the
way they're written. `assets/fonts/KleeOne-SemiBold-hiragana.ttf` is a hiragana-only subset (SIL Open Font
License, see `assets/fonts/KleeOne-OFL.txt`).

# To run locally

1. clone with submodules

```bash
git clone --recurse-submodules [url]
```

2. set python venv

```bash
source environment/bin/activate
```

3. install cython

```bash
sudo apt update
sudo apt install cython3
```

4. install ledmatrix library (https://github.com/hzeller/rpi-rgb-led-matrix/tree/master/bindings/python)

```bash
cd submodules/matrix/
sudo apt-get update && sudo apt-get install python3-dev cython3 -y
make build-python
sudo make install-python
```
