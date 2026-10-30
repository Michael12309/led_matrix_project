import random
from collections import deque, namedtuple
from datetime import timedelta

from kana import BY_CHAR, LESSONS, LOOKALIKES, WORDS, split_units, word_romaji

# Leitner-style spaced repetition for a board with no buttons: a kana moves up a box
# as the days since its lesson unlocked pass each of these marks...
BOX_DAYS = (1, 3, 7, 14, 30)
# ...and each box comes up half as often as the one below it, so new kana get drilled
# while old ones keep returning at a slower pace.
# Familiar kana get less thinking time, to push towards instant recognition.
THINK_SCALE = (1.0, 1.0, 0.8, 0.8, 0.6, 0.6)
# Show the mnemonic while a kana is in box 0 or 1 (its first 3 days)
HINT_MAX_BOX = 1

WORD_CHANCE = 0.15
PAIR_CHANCE = 0.10
PROGRESS_EVERY = 40  # cards
PROGRESS_SECONDS = 6

Progress = namedtuple("Progress", ["day", "lesson", "lessons", "known", "total", "newest", "next_in"])


class Card(object):
    """One flash card: the prompt shows for `think` seconds, then the answer for at least `answer` seconds."""

    def __init__(self, kind, think, answer, kana=(), word=None, hint=None, new=False, progress=None):
        self.kind = kind  # "kana", "pair", "word" or "progress"
        self.think = think
        self.answer = answer
        self.kana = kana  # the Kana tested by a kana or pair card
        self.word = word  # (hiragana, romaji) for a word card
        self.hint = hint  # mnemonic, look-alike tip or word meaning
        self.new = new
        self.progress = progress


class Scheduler(object):
    def __init__(self, start, days_per_lesson, think, answer, rng=None):
        self.start = start
        self.days_per_lesson = days_per_lesson
        self.think = think
        self.answer = answer
        self.rng = rng or random.Random()
        self.words = [(word, meaning, split_units(word)) for word, meaning in WORDS]
        self.count = 0
        self.lessons_shown = 0
        self.history = deque(maxlen=30)  # the last 30 cards, so pairs and words don't repeat too soon
        self.recent_kana = deque(maxlen=8)

    def days(self, now):
        return (now - self.start).total_seconds() / 86400

    def lessons_unlocked(self, now):
        return max(1, min(len(LESSONS), int(self.days(now) // self.days_per_lesson) + 1))

    def box(self, kana, now):
        age = self.days(now) - kana.lesson * self.days_per_lesson
        return sum(age >= days for days in BOX_DAYS)

    def next_card(self, now):
        unlocked = self.lessons_unlocked(now)
        pool = [k for lesson in LESSONS[:unlocked] for k in lesson]
        weights = {k.char: 2 ** (len(BOX_DAYS) - self.box(k, now)) for k in pool}

        self.count += 1
        # Show progress at startup, whenever a new lesson unlocks, and every so often
        if unlocked != self.lessons_shown or self.count % PROGRESS_EVERY == 0:
            self.lessons_shown = unlocked
            self.history.append(None)
            return self.progress_card(now, unlocked, pool)

        card = None
        roll = self.rng.random()
        if roll < WORD_CHANCE:
            card = self.word_card(weights)
        elif roll < WORD_CHANCE + PAIR_CHANCE:
            card = self.pair_card(weights, now)
        return card or self.kana_card(pool, weights, now)

    def kana_card(self, pool, weights, now):
        # Keep a gap between repeats; the gap shrinks when only a few kana are unlocked
        gap = min(len(self.recent_kana), len(pool) // 2)
        recent = set(list(self.recent_kana)[len(self.recent_kana) - gap:])
        choices = [k for k in pool if k.char not in recent]
        kana = self.rng.choices(choices, [weights[k.char] for k in choices])[0]
        self.history.append(kana.char)
        self.recent_kana.append(kana.char)

        box = self.box(kana, now)
        hint = kana.hint if box <= HINT_MAX_BOX else None
        return Card("kana", self.think * THINK_SCALE[box], self.answer, kana=[kana], hint=hint, new=box == 0)

    def pair_card(self, weights, now):
        """Two look-alike kana side by side, to practise telling them apart."""
        pairs = [(a, b, tip) for a, b, tip in LOOKALIKES
                 if a in weights and b in weights and (a, b) not in self.history]
        if not pairs:
            return None
        a, b, tip = self.rng.choices(pairs, [max(weights[a], weights[b]) for a, b, _ in pairs])[0]
        self.history.append((a, b))
        self.recent_kana.extend((a, b))

        pair = [BY_CHAR[a], BY_CHAR[b]]
        self.rng.shuffle(pair)  # so position isn't a clue
        return Card("pair", self.think, self.answer + 1, kana=pair, hint=tip)

    def word_card(self, weights):
        """A real word made only of unlocked kana, favouring words that use the newest ones."""
        words = [(word, meaning, max(weights[u] for u in units)) for word, meaning, units in self.words
                 if all(u in weights for u in units) and word not in self.history]
        if not words:
            return None
        word, meaning, _ = self.rng.choices(words, [weight for _, _, weight in words])[0]
        self.history.append(word)
        return Card("word", self.think + 1, self.answer + 2, word=(word, word_romaji(word)), hint=meaning)

    def progress_card(self, now, unlocked, pool):
        next_in = None
        if unlocked < len(LESSONS):
            next_in = self.start + timedelta(days=unlocked * self.days_per_lesson) - now
        progress = Progress(day=max(1, int(self.days(now)) + 1), lesson=unlocked, lessons=len(LESSONS),
                            known=len(pool), total=len(BY_CHAR), newest=LESSONS[unlocked - 1], next_in=next_in)
        return Card("progress", 0, PROGRESS_SECONDS, progress=progress)
