from PIL import BdfFontFile

fp = open("5x7.bdf", "rb")
p = BdfFontFile.BdfFontFile(fp)
p.save("5x7")
fp.close()
