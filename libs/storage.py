from pathlib import Path
from PIL import Image
import itertools


class Storage(object):

    def __init__(self, path, extensions):
        self._path = Path(path)
        self._extensions = extensions

    def get_current(self):
        g = itertools.chain.from_iterable(self._path.glob(e) for e in self._extensions)
        flist = sorted(g)
        if len(flist) == 0:
            return None
        fname = flist[0]
        img = Image.open(fname)
        img.load()
        return img
