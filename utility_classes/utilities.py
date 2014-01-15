##############################################################################
import re

from kivy.config import Config

##############################################################################

class Utilities(object):

    # ------------------------------------------------------------------------
    # Class variables

    window_width = Config.getint('graphics', 'width')
    window_height = Config.getint('graphics', 'height')

    # ------------------------------------------------------------------------

    # Horizontally (make sure nothing goes out of the screen)
    @staticmethod
    def clamp_x(x):
        if x < 0:
            return 0
        if x > Utilities.window_width:
            print Utilities.window_width
            return Utilities.window_width
        return x

    # ------------------------------------------------------------------------

    # Vertically (make sure nothing goes out of the screen)
    @staticmethod
    def clamp_y(y):
        if y < 0:
            return 0
        if y > Utilities.window_height:
            return Utilities.window_height
        return y

    # ------------------------------------------------------------------------

    # Clamp for screen (stay within)
    @staticmethod
    def clamp(*args):
        x, y = args[0], args[1]
        return Utilities.clamp_x(x), Utilities.clamp_y(y)

    # ------------------------------------------------------------------------

    @staticmethod
    def reverse_enum(L):
        for index in reversed(xrange(len(L))):
            yield index, L[index]

    # ------------------------------------------------------------------------

    # From here: http://stackoverflow.com/questions/715417/converting-from-a-string-to-boolean-in-python
    @staticmethod
    def str2bool(v):
        return v.lower() in ("yes", "true", "t", "1")

    # ------------------------------------------------------------------------

    # From here: http://stackoverflow.com/questions/4296249/how-do-i-convert-a-hex-triplet-to-an-rgb-tuple-and-back
    @staticmethod
    def triplet(rgb):
        return format((rgb[0]<<16)|(rgb[1]<<8)|rgb[2], '06x')

    # ------------------------------------------------------------------------

    # From here: http://stackoverflow.com/questions/4836710/does-python-have-a-built-in-function-for-string-natural-sort
    # i.e. given a list of items like "1,2,3,10,11, etc"
    # a regular lexicographic sort would produce 1,10,11,2,3
    # which is not what we want
    # instead we want
    # 1,2,3,10,11
    @staticmethod
    def natural_sort(l):
        convert = lambda text: int(text) if text.isdigit() else text.lower()
        alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
        return sorted(l, key = alphanum_key)

    # ------------------------------------------------------------------------

##############################################################################