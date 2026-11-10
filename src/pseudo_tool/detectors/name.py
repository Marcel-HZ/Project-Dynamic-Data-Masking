import jieba.posseg as pseg
import re

from .base import DetectorBase, Hit
from ..config import SURNAMES, COMPOUND_SURNAMES, NAME_TAIL_CHARS, CAPITAL_NUMBER_CHARS

ADDRESS_CHARS = set("省市县镇乡村路街道德巷号栋室楼层座园苑府庭湾里弄")
ORG_SUFFIXES = ["支行", "分行", "总行", "银行", "公司", "集团", "厂", "店", "馆", "院", "校", "所", "局", "处", "科", "部", "委", "办", "中心", "医院", "学校", "大学", "学院", "事务所", "研究院", "营业部", "办事处", "管委会", "工作室", "门市部"]


class NameDetector(DetectorBase):
    def __init__(self):
        self.overlap_provider = lambda: set()

    def set_overlap_provider(self, provider):
        self.overlap_provider = provider

    def _is_name(self, word):
        if len(word) < 2:
            return False
        if len(word) == 2:
            return word[0] in SURNAMES and word[1] in NAME_TAIL_CHARS
        if len(word) == 4:
            if word[:2] in COMPOUND_SURNAMES:
                return (word[2] in NAME_TAIL_CHARS or word[3] in NAME_TAIL_CHARS)
            return False
        if len(word) == 3:
            if word[:2] in COMPOUND_SURNAMES:
                return (word[2] in NAME_TAIL_CHARS)
            if word[0] in SURNAMES:
                return (word[1] in NAME_TAIL_CHARS or word[2] in NAME_TAIL_CHARS)
            return False
        return False

    def detect(self, text: str) -> list[Hit]:
        overlaps = self.overlap_provider() if callable(self.overlap_provider) else set()
        hits = []
        seen = set()
        for word, flag in pseg.cut(text):
            if flag not in ("nr", "nrfg", "nrt"):
                continue
            if not self._is_name(word):
                continue
            idx = text.find(word)
            left = text[max(0, idx - 2):idx]
            right = text[idx + len(word):idx + len(word) + 4]
            if any(c in left for c in ADDRESS_CHARS):
                continue
            if any(suf in right for suf in ORG_SUFFIXES):
                continue
            if word in overlaps:
                continue
            # skip capital numbers like "伍万圆整"
            if all(ch in CAPITAL_NUMBER_CHARS for ch in word):
                continue
            if word in seen:
                continue
            seen.add(word)
            hits.append(Hit(text=word, type="NAME"))
        # fallback for compound surnames segmented separately by jieba
        for cs in COMPOUND_SURNAMES:
            for m in re.finditer(re.escape(cs) + r"([" + "".join(NAME_TAIL_CHARS) + r"]{1,2})", text):
                name = m.group(0)
                if name in seen or name in overlaps:
                    continue
                seen.add(name)
                hits.append(Hit(text=name, type="NAME"))
        return hits





