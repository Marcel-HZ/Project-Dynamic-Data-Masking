import re

from .base import DetectorBase, Hit

_PATTERN = re.compile(r'(?:[\u4e00-\u9fa5]{2,8}(?:省|自治区|市))?[\u4e00-\u9fa5]{2,10}(?:区|县|市)[\u4e00-\u9fa5]{0,20}(?:路|街|道|巷)[\u4e00-\u9fa5\d]{0,10}(?:号|栋|室|单元)?')


class AddressDetector(DetectorBase):
    def detect(self, text: str) -> list[Hit]:
        hits = []
        seen = set()
        for m in _PATTERN.finditer(text):
            val = m.group(0)
            if len(val) < 6:
                continue
            if val in seen:
                continue
            seen.add(val)
            hits.append(Hit(text=val, type="ADDRESS"))
        # simplified fallback
        for m in re.finditer(r'[\u4e00-\u9fa5\d]{6,}', text):
            val = m.group(0)
            if any(k in val for k in ("省", "市", "区", "路", "街", "号")) and val not in seen:
                seen.add(val)
                hits.append(Hit(text=val, type="ADDRESS"))
        return hits
