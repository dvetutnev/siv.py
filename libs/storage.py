from pathlib import Path
from PIL import Image
import itertools


class Storage(object):

    def __init__(self, path, extensions):
        self._path = Path(path)
        self._extensions = extensions

    def get(self, offset):
        if offset < 0:
            return None

        if offset == 0:
            g = itertools.chain.from_iterable(self._path.glob(e) for e in self._extensions)
            self._flist = sorted(g)

        flist = self._flist[offset::]
        for fname in flist:
            try:
                img = Image.open(fname)
                img.load()
                return img
            except OSError:
                continue

        return None
