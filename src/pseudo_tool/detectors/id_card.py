import re

from .base import DetectorBase, Hit


class IdCardDetector(DetectorBase):
    def detect(self, text: str) -> list[Hit]:
        hits = []
        for m in re.finditer(r"\b\d{15}\b", text):
            hits.append(Hit(text=m.group(0), type="ID"))
        for m in re.finditer(r"\b\d{17}[\dXx]\b", text):
            hits.append(Hit(text=m.group(0), type="ID"))
        # dedup
        seen = set()
        out = []
        for h in hits:
            if h.text in seen:
                continue
            seen.add(h.text)
            out.append(h)
        return out


class UnifiedSocialCreditCodeDetector(DetectorBase):
    def detect(self, text: str) -> list[Hit]:
        hits = []
        seen = set()
        for m in re.finditer(r"\b[0-9A-Z]{2}\d{6}[0-9A-Z]{10}\b", text):
            if m.group(0) in seen:
                continue
            seen.add(m.group(0))
            hits.append(Hit(text=m.group(0), type="USCC"))
        return hits
