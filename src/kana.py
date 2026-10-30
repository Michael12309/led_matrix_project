import unicodedata
from collections import namedtuple

Kana = namedtuple("Kana", ["char", "romaji", "hint", "lesson"])

# Basic hiragana in the order they're traditionally taught (rows of the gojuon chart).
# Hints are shape -> sound mnemonics; the capitalised part is the sound.
BASIC_LESSONS = [
    [("あ", "a", "AHH! a cross caught in a lasso"),
     ("い", "i", "two strokes like 'ii' (EE)"),
     ("う", "u", "a sideways U wearing a hat"),
     ("え", "e", "a ninja kick: EH-yah!"),
     ("お", "o", "OH! a golf swing, ball flies")],
    [("か", "ka", "a KArate chop with a spark"),
     ("き", "ki", "a KEY with two teeth"),
     ("く", "ku", "a bird's beak: COO COO"),
     ("け", "ke", "a KEG tipped by a post"),
     ("こ", "ko", "two KOi swimming side by side")],
    [("さ", "sa", "a key missing a tooth: SAd"),
     ("し", "shi", "a fishhook: SHE is fishing"),
     ("す", "su", "a SUspended swing with a loop"),
     ("せ", "se", "a mouth with a fang: SAY ahh"),
     ("そ", "so", "a zigzag stitch: SEW (so)")],
    [("た", "ta", "a 't' next to an 'a': TA"),
     ("ち", "chi", "a chubby guy on a CHIn-up bar"),
     ("つ", "tsu", "a big TSUnami wave"),
     ("て", "te", "a curvy capital T: TE"),
     ("と", "to", "a TOE with a splinter in it")],
    [("な", "na", "a NAughty knot tied to a cross"),
     ("に", "ni", "a NEEdle and two threads"),
     ("ぬ", "nu", "NOOdles with a loop at the end"),
     ("ね", "ne", "NEko the cat, tail curled up"),
     ("の", "no", "a NO-entry sign")],
    [("は", "ha", "a cursive 'h' + 'a': HA"),
     ("ひ", "hi", "a big grin: HEE hee!"),
     ("ふ", "fu", "Mt. FUji with puffs of cloud"),
     ("へ", "he", "a tiny hill: HEY, climb me!"),
     ("ほ", "ho", "HO HO HO: Santa's belts + belly")],
    [("ま", "ma", "a MAypole with a knot"),
     ("み", "mi", "looks like '21': ME at 21!"),
     ("む", "mu", "a cow's face saying MOO"),
     ("め", "me", "an eye - ME means eye"),
     ("も", "mo", "a fishhook catching MOre fish")],
    [("や", "ya", "a YAk with big horns"),
     ("ゆ", "yu", "a fish swimming: YUmmy"),
     ("よ", "yo", "a YO-yo on a string")],
    [("ら", "ra", "a RAbbit sitting up"),
     ("り", "ri", "two REEds by a river"),
     ("る", "ru", "a winding ROUte with a loop"),
     ("れ", "re", "a man kneeling to REst"),
     ("ろ", "ro", "a ROad with no loop")],
    [("わ", "wa", "WAh! ne lost its loop"),
     ("を", "wo", "WOah! someone tripping"),
     ("ん", "n", "a cursive lowercase 'n'")],
]

# Kana made by adding ten-ten (dakuten) or maru (handakuten) to a basic kana.
VOICED_LESSONS = [
    [("が", "ga"), ("ぎ", "gi"), ("ぐ", "gu"), ("げ", "ge"), ("ご", "go")],
    [("ざ", "za"), ("じ", "ji"), ("ず", "zu"), ("ぜ", "ze"), ("ぞ", "zo")],
    [("だ", "da"), ("ぢ", "ji"), ("づ", "zu"), ("で", "de"), ("ど", "do")],
    [("ば", "ba"), ("び", "bi"), ("ぶ", "bu"), ("べ", "be"), ("ぼ", "bo")],
    [("ぱ", "pa"), ("ぴ", "pi"), ("ぷ", "pu"), ("ぺ", "pe"), ("ぽ", "po")],
]
RARE = {"ぢ", "づ"}

# Kana combined with a small ya / yu / yo (yoon).
COMBO_LESSONS = [
    [("きゃ", "kya"), ("きゅ", "kyu"), ("きょ", "kyo"), ("しゃ", "sha"), ("しゅ", "shu"), ("しょ", "sho")],
    [("ちゃ", "cha"), ("ちゅ", "chu"), ("ちょ", "cho"), ("にゃ", "nya"), ("にゅ", "nyu"), ("にょ", "nyo")],
    [("ひゃ", "hya"), ("ひゅ", "hyu"), ("ひょ", "hyo"), ("みゃ", "mya"), ("みゅ", "myu"), ("みょ", "myo")],
    [("りゃ", "rya"), ("りゅ", "ryu"), ("りょ", "ryo"), ("ぎゃ", "gya"), ("ぎゅ", "gyu"), ("ぎょ", "gyo")],
    [("じゃ", "ja"), ("じゅ", "ju"), ("じょ", "jo"), ("びゃ", "bya"), ("びゅ", "byu"), ("びょ", "byo")],
    [("ぴゃ", "pya"), ("ぴゅ", "pyu"), ("ぴょ", "pyo")],
]
SMALL = {"ゃ": "ya", "ゅ": "yu", "ょ": "yo"}

# Characters that are easy to mix up, with a tip for telling them apart.
LOOKALIKES = [
    ("あ", "お", "o has a dot at the top right"),
    ("い", "り", "i: left stroke long, ri: right"),
    ("う", "ら", "ra has a stem on its left"),
    ("き", "さ", "ki has 2 bars, sa has 1"),
    ("さ", "ち", "sa opens right, chi opens left"),
    ("ち", "ら", "chi: crossed bar, ra: a dash"),
    ("こ", "に", "ni = a stick + ko"),
    ("た", "な", "ta ends in ko, na in a loop"),
    ("け", "は", "ha has a loop at the bottom"),
    ("は", "ほ", "ho: 2 bars and a capped top"),
    ("ほ", "ま", "ho has a stick on its left"),
    ("ま", "も", "ma loops, mo hooks up"),
    ("ぬ", "め", "nu ends in a loop, me doesn't"),
    ("ね", "れ", "ne ends in a loop, re kicks out"),
    ("ね", "わ", "ne ends in a loop, wa curls in"),
    ("れ", "わ", "re kicks out, wa curls in"),
    ("る", "ろ", "ru has a loop, ro doesn't"),
    ("し", "つ", "shi goes down, tsu goes across"),
    ("ば", "ぱ", "2 dots = b, circle = p"),
    ("び", "ぴ", "2 dots = b, circle = p"),
    ("ぶ", "ぷ", "2 dots = b, circle = p"),
    ("べ", "ぺ", "2 dots = b, circle = p"),
    ("ぼ", "ぽ", "2 dots = b, circle = p"),
]

# Everyday words for reading practice; each appears once all of its kana are unlocked.
WORDS = [
    ("あい", "love"), ("あお", "blue"), ("いえ", "house"), ("うえ", "up, above"), ("いいえ", "no"),
    ("あか", "red"), ("あき", "autumn"), ("いか", "squid"), ("いけ", "pond"), ("えき", "station"),
    ("かお", "face"), ("こえ", "voice"), ("ここ", "here"), ("あさ", "morning"), ("あし", "leg, foot"),
    ("いす", "chair"), ("うし", "cow"), ("おかし", "sweets"), ("かさ", "umbrella"), ("しお", "salt"),
    ("しか", "deer"), ("すし", "sushi"), ("すいか", "watermelon"), ("せき", "seat"), ("そこ", "there"),
    ("あたま", "head"), ("いつ", "when"), ("うた", "song"), ("うち", "home"), ("きた", "north"),
    ("くち", "mouth"), ("くつ", "shoes"), ("した", "below"), ("そと", "outside"), ("たこ", "octopus"),
    ("たけ", "bamboo"), ("つき", "moon"), ("つくえ", "desk"), ("とし", "year"), ("あつい", "hot"),
    ("あな", "hole"), ("あに", "big brother"), ("あね", "big sister"), ("いぬ", "dog"), ("かに", "crab"),
    ("きつね", "fox"), ("きのこ", "mushroom"), ("さかな", "fish"), ("なつ", "summer"), ("にく", "meat"),
    ("にし", "west"), ("ねこ", "cat"), ("ねつ", "fever"), ("なに", "what"), ("たぬき", "raccoon dog"),
    ("はな", "flower, nose"), ("はし", "chopsticks"), ("ひと", "person"), ("ふね", "boat"),
    ("ふく", "clothes"), ("へそ", "belly button"), ("ほし", "star"), ("ほね", "bone"), ("はい", "yes"),
    ("ひこうき", "airplane"), ("たかい", "tall, pricey"), ("いま", "now"), ("うま", "horse"),
    ("うみ", "sea"), ("おかね", "money"), ("かみ", "paper, hair"), ("くま", "bear"), ("くも", "cloud"),
    ("こめ", "rice"), ("さしみ", "sashimi"), ("まち", "town"), ("まめ", "bean"), ("みみ", "ear"),
    ("みせ", "shop"), ("みち", "road"), ("みなみ", "south"), ("むし", "bug"), ("むね", "chest"),
    ("もも", "peach"), ("あめ", "rain"), ("さむい", "cold"), ("おもい", "heavy"), ("きもの", "kimono"),
    ("いもうと", "little sister"), ("おとうと", "little brother"), ("すもう", "sumo"),
    ("やま", "mountain"), ("やさい", "vegetables"), ("ゆき", "snow"), ("ゆめ", "dream"), ("ふゆ", "winter"),
    ("へや", "room"), ("やすい", "cheap"), ("はやい", "fast, early"), ("ねむい", "sleepy"),
    ("あり", "ant"), ("いろ", "color"), ("くるま", "car"), ("くろ", "black"), ("こころ", "heart"),
    ("さくら", "cherry blossom"), ("さる", "monkey"), ("しろ", "white"), ("そら", "sky"), ("てら", "temple"),
    ("とり", "bird"), ("のり", "seaweed"), ("はる", "spring"), ("ひる", "noon"), ("もり", "forest"),
    ("よる", "night"), ("りす", "squirrel"), ("とけい", "clock"),
    ("かわ", "river"), ("わたし", "I, me"), ("わに", "crocodile"), ("ほん", "book"), ("にほん", "Japan"),
    ("みかん", "mandarin"), ("せんせい", "teacher"), ("てんき", "weather"), ("おんな", "woman"),
    ("かわいい", "cute"), ("おいしい", "delicious"), ("おとこ", "man"),
    ("かぎ", "key"), ("かがみ", "mirror"), ("りんご", "apple"), ("たまご", "egg"), ("ごはん", "rice, meal"),
    ("げんき", "lively, well"), ("がくせい", "student"), ("めがね", "glasses"), ("うさぎ", "rabbit"),
    ("おにぎり", "rice ball"), ("にほんご", "Japanese"),
    ("かぜ", "wind"), ("かぞく", "family"), ("ぞう", "elephant"), ("みず", "water"), ("ねずみ", "mouse"),
    ("ひつじ", "sheep"), ("かんじ", "kanji"), ("ちず", "map"),
    ("からだ", "body"), ("だれ", "who"), ("どこ", "where"), ("こども", "child"), ("でんわ", "phone"),
    ("ともだち", "friend"), ("まど", "window"), ("くだもの", "fruit"),
    ("ぶた", "pig"), ("ゆび", "finger"), ("へび", "snake"), ("かばん", "bag"), ("しんぶん", "newspaper"),
    ("こんぶ", "kelp"), ("どうぶつ", "animal"),
    ("えんぴつ", "pencil"), ("さんぽ", "a walk"), ("てんぷら", "tempura"), ("たんぽぽ", "dandelion"),
    ("ぴかぴか", "sparkly"),
    ("きょう", "today"), ("きゃく", "guest"), ("やきゅう", "baseball"), ("きゅうり", "cucumber"),
    ("しゃしん", "photo"), ("じしょ", "dictionary"), ("いしゃ", "doctor"), ("かいしゃ", "company"),
    ("しょうゆ", "soy sauce"), ("しゅみ", "hobby"), ("おちゃ", "tea"), ("ちょう", "butterfly"),
    ("ちゃわん", "rice bowl"), ("ちゅうい", "caution"), ("こうちゃ", "black tea"), ("ひゃく", "hundred"),
    ("みゃく", "pulse"), ("みょうじ", "surname"), ("りゅう", "dragon"), ("りょこう", "travel"),
    ("りょうり", "cooking"), ("ぎょうざ", "dumplings"), ("ぎゃく", "opposite"), ("きんぎょ", "goldfish"),
    ("にんぎょ", "mermaid"), ("でんしゃ", "train"), ("じゅう", "ten"), ("じょうず", "skillful"),
    ("びょうき", "sickness"), ("しょくじ", "meal"),
]


def _build_lessons():
    lessons = [[Kana(c, r, h, i) for c, r, h in lesson] for i, lesson in enumerate(BASIC_LESSONS)]
    romaji = {k.char: k.romaji for lesson in lessons for k in lesson}

    for chars in VOICED_LESSONS:
        lesson = []
        for char, r in chars:
            base, mark = unicodedata.normalize("NFD", char)
            mark = "ten-ten" if mark == "゙" else "maru"
            hint = f"{romaji[base]} + {mark} = {r}" + (" (rare)" if char in RARE else "")
            lesson.append(Kana(char, r, hint, len(lessons)))
            romaji[char] = r
        lessons.append(lesson)

    for chars in COMBO_LESSONS:
        lesson = [Kana(c, r, f"{romaji[c[0]]} + small {SMALL[c[1]]} = {r}", len(lessons)) for c, r in chars]
        lessons.append(lesson)
    return lessons


LESSONS = _build_lessons()
BY_CHAR = {k.char: k for lesson in LESSONS for k in lesson}


def split_units(word):
    """Split a word into flash card units, keeping small ya/yu/yo with the kana before it."""
    units = []
    for char in word:
        if char in SMALL and units:
            units[-1] += char
        else:
            units.append(char)
    return units


def word_romaji(word):
    return "".join(BY_CHAR[unit].romaji for unit in split_units(word))
