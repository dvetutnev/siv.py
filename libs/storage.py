from pathlib import Path
from PIL import Image
import itertools


class Storage(object):

    def __init__(self, path, extensions):
        self._path = Path(path)
        self._extensions = extensions
        self._fname_current = None

    def get(self, offset):
        if offset == 0:
            g = itertools.chain.from_iterable(self._path.glob(e) for e in self._extensions)
            self._flist = sorted(g)
            if not self._flist:
                return None
            if self._fname_current is None:
                self._fname_current = self._flist[0]

        idx_current = self._find_idx_current()
        if idx_current + offset < 0:
            return None

        flist = self._flist[idx_current + offset::]
        for fname in flist:
            try:
                img = Image.open(fname)
                img.load()
                return img
            except OSError:
                continue

        return None

    def step_next(self):
        idx = self._find_idx_current()
        if len(self._flist) - 1 > idx:
            self._fname_current = self._flist[idx + 1]

    def _find_idx_current(self):
        idx = len(self._flist) - 1
        for fname in self._flist:
            if fname >= self._fname_current:
                idx = self._flist.index(fname)
                break
        return idx
