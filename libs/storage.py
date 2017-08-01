from pathlib import Path
from PIL import Image
import itertools


class Storage(object):

    def __init__(self, path, extensions):
        self._path = Path(path)
        self._extensions = extensions
        self._flist = None

    def get_previous(self, offset):
        return None

    def get_current(self):
        if self._flist is None:
            g = itertools.chain.from_iterable(self._path.glob(e) for e in self._extensions)
            self._flist = sorted(g)
        if len(self._flist) == 0:
            return None
        fname = self._flist[0]
        img = Image.open(fname)
        img.load()
        return img

    def get_next(self, offset):
        if self._flist is None:
            g = itertools.chain.from_iterable(self._path.glob(e) for e in self._extensions)
            self._flist = sorted(g)
        if offset + 1 >= len(self._flist):
            return None
        fname = self._flist[offset + 1]
        img = Image.open(fname)
        img.load()
        return img
