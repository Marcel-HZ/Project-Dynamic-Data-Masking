import json
from pathlib import Path

from cryptography.fernet import Fernet


class CryptoStore:
    def __init__(self, map_file, key_file):
        self.map_file = Path(map_file)
        self.key_file = Path(key_file)

    def _get_key(self) -> bytes:
        if self.key_file.exists():
            return self.key_file.read_bytes()
        key = Fernet.generate_key()
        self.key_file.parent.mkdir(parents=True, exist_ok=True)
        self.key_file.write_bytes(key)
        return key

    def load(self) -> dict:
        if not self.map_file.exists():
            return {"forward": {}, "reverse": {}, "counters": {}}
        key = self._get_key()
        f = Fernet(key)
        data = f.decrypt(self.map_file.read_bytes())
        return json.loads(data.decode("utf-8"))

    def save(self, data: dict) -> None:
        self.map_file.parent.mkdir(parents=True, exist_ok=True)
        key = self._get_key()
        f = Fernet(key)
        payload = json.dumps(data).encode("utf-8")
        self.map_file.write_bytes(f.encrypt(payload))

    def destroy(self) -> None:
        for p in (self.map_file, self.key_file):
            try:
                p.unlink()
            except FileNotFoundError:
                pass
