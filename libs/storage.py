from pathlib import Path
from PIL import Image
import itertools


class Storage(object):

    def __init__(self, path, extensions):
        self._path = Path(path)
        self._extensions = extensions
        self._idx_current = 0

    def get(self, offset):
        if offset == 0:
            g = itertools.chain.from_iterable(self._path.glob(e) for e in self._extensions)
            self._flist = sorted(g)
            if not self._flist:
                return None

        if self._idx_current + offset < 0:
            return None

        flist = self._flist[self._idx_current + offset::]
        for fname in flist:
            try:
                img = Image.open(fname)
                img.load()
                return img
            except OSError:
                continue

        return None

    def step_next(self):
        if len(self._flist) - 1 > self._idx_current:
            self._idx_current += 1
