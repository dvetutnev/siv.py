from pathlib import Path
from PIL import Image
import itertools


class Storage(object):

    def __init__(self, path, extensions):
        self._path = Path(path)
        self._extensions = extensions

    def get(self, offest):
        g = itertools.chain.from_iterable(self._path.glob(e) for e in self._extensions)
        flist = sorted(g)
        for fname in flist:
            try:
                img = Image.open(fname)
                img.load()
                return img
            except:
                continue
        return None
