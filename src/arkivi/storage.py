import shutil
from pathlib import Path
from typing import BinaryIO, Iterable


class Storage:

    __slots__ = ('root',)

    def __init__(self, root: str):
        self.root = Path(root)

    def persist(self, name: str, fobj: BinaryIO, folder: Path) -> bool:
        jailed = (self.root / folder / Path(name)).resolve()
        jailed.parent.mkdir(mode=0o755, parents=True, exist_ok=True)
        if not jailed.exists():
            with jailed.open('wb') as fd:
                shutil.copyfileobj(fobj, fd)
            return True
        return False

    def list(self, folder: Path) -> Iterable[Path]:
        jailed = (self.root / folder).resolve()
        if not jailed.exists():
            return []
        return (path for path in jailed.iterdir() if path.is_file())
