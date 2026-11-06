import re

from .base import DetectorBase, Hit


class EmailDetector(DetectorBase):
    def detect(self, text: str) -> list[Hit]:
        hits = []
        seen = set()
        for m in re.finditer(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text):
            if m.group(0) in seen:
                continue
            seen.add(m.group(0))
            hits.append(Hit(text=m.group(0), type="EMAIL"))
        return hits
