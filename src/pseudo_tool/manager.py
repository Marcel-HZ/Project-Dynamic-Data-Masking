from pathlib import Path

from .config import MAP_FILE, KEY_FILE, PSEUDO_TEMPLATES, COMPOUND_SURNAMES
from .crypto_store import CryptoStore


class PseudonymManager:
    def __init__(self, map_file=None, key_file=None):
        self.map_file = Path(map_file) if map_file is not None else MAP_FILE
        self.key_file = Path(key_file) if key_file is not None else KEY_FILE
        self.store = CryptoStore(self.map_file, self.key_file)
        data = self.store.load()
        self.forward = data.get("forward", {})
        self.reverse = data.get("reverse", {})
        self.counters = data.get("counters", {})

    def get_pseudonym(self, real: str, ptype: str) -> str:
        if real in self.forward:
            return self.forward[real]
        n = self.counters.get(ptype, 0) + 1
        while True:
            if ptype == "NAME":
                if real[:2] in COMPOUND_SURNAMES:
                    pseudo = f"{real[:2]}某{n}"
                else:
                    pseudo = f"{real[:1]}某{n}"
            else:
                template = PSEUDO_TEMPLATES[ptype]
                pseudo = template.format(n=n)
            # collision check against existing forward keys/values
            if pseudo in self.forward.values() or pseudo in self.forward:
                n += 1
                continue
            if pseudo == real:
                n += 1
                continue
            break
        self.forward[real] = pseudo
        self.reverse[pseudo] = real
        self.counters[ptype] = n
        return pseudo

    def restore(self, pseudo: str) -> str:
        return self.reverse.get(pseudo, pseudo)

    def reverse_map(self) -> dict:
        return dict(self.reverse)

    def save(self) -> None:
        self.store.save({"forward": self.forward, "reverse": self.reverse, "counters": self.counters})

    def clear(self) -> None:
        self.forward.clear()
        self.reverse.clear()
        self.counters.clear()
        self.store.destroy()


