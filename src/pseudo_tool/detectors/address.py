import re

from .base import DetectorBase, Hit

ORG_SUFFIXES = ["联合会", "协会", "学会", "局", "委员会", "办公室", "办公厅", "办事处", "中心",
    "研究院", "研究所", "大学", "学院", "学校", "医院", "银行", "公司", "集团",
    "人民法院", "人民检察院"]

_PATTERN = re.compile(r'(?:[一-龥]{2,8}(?:省|自治区|市))?[一-龥]{2,10}(?:区|县|市)[一-龥]{0,20}(?:路|街|道|巷)[一-龥\d]{0,10}(?:号|栋|室|单元)?')


class AddressDetector(DetectorBase):
    def detect(self, text: str) -> list[Hit]:
        hits = []
        seen = set()
        for m in _PATTERN.finditer(text):
            val = m.group(0)
            if len(val) < 6:
                continue
            # skip if ends with ORG suffix
            if any(val.endswith(suf) for suf in ORG_SUFFIXES):
                continue
            if val in seen:
                continue
            seen.add(val)
            hits.append(Hit(text=val, type="ADDRESS"))
        # simplified fallback
        for m in re.finditer(r'[一-龥\d]{6,}', text):
            val = m.group(0)
            if any(k in val for k in ("省", "市", "区", "路", "街", "号")) and val not in seen:
                if any(val.endswith(suf) for suf in ORG_SUFFIXES):
                    continue
                seen.add(val)
                hits.append(Hit(text=val, type="ADDRESS"))
        return hits
