import os

def readtext(filepath):
    try:
        file = open(filepath,'r')
        lines = file.read()
        file.close()
        return lines
    except:
        return None

def readFromMedia(MEDIA_ROOT,filename):
    try:
        file = open(os.path.join(MEDIA_ROOT,filename))
        lines = file.read()
        file.close()
        return lines
    except:
        return None
