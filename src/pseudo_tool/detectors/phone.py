import re

from .base import DetectorBase, Hit


class PhoneDetector(DetectorBase):
    def detect(self, text: str) -> list[Hit]:
        hits = []
        seen = set()
        for m in re.finditer(r"(?<![A-Za-z0-9])1[3-9]\d{9}(?![A-Za-z0-9])", text):
            if m.group(0) in seen:
                continue
            seen.add(m.group(0))
            hits.append(Hit(text=m.group(0), type="PHONE"))
        return hits
