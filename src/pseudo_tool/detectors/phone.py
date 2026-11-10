import re

from .base import DetectorBase, Hit


class PhoneDetector(DetectorBase):
    def detect(self, text: str) -> list[Hit]:
        hits = []
        seen = set()
        # mobile
        for m in re.finditer(r"(?<![A-Za-z0-9])1[3-9]\d{9}(?![A-Za-z0-9])", text):
            if m.group(0) in seen:
                continue
            seen.add(m.group(0))
            hits.append(Hit(text=m.group(0), type="PHONE"))
        # landline: 0xxx-xxxxxxx or 0xxx-xxxxxxx-xxxx
        for m in re.finditer(r"(?<![A-Za-z0-9])0\d{2,3}-?\d{7,8}(?:-\d{1,4})?(?![A-Za-z0-9])", text):
            if m.group(0) in seen:
                continue
            seen.add(m.group(0))
            hits.append(Hit(text=m.group(0), type="PHONE"))
        return hits
