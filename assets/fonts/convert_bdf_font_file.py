import sys
from PIL import BdfFontFile

# Usage (from this folder): python convert_bdf_font_file.py 5x7 9x15B
for name in sys.argv[1:] or ["5x7"]:
    fp = open(name + ".bdf", "rb")
    p = BdfFontFile.BdfFontFile(fp)
    p.save(name)
    fp.close()
