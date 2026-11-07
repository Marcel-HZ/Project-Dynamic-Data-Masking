from .base import DetectorBase, Hit
from ..config import ORG_SUFFIX_MAP

# build flat suffix -> subtype, longest first
_SUFFIX_TO_TYPE = {}
for subtype, suffixes in ORG_SUFFIX_MAP.items():
    for suf in suffixes:
        _SUFFIX_TO_TYPE[suf] = subtype
_ALL_SUFFIXES = sorted(_SUFFIX_TO_TYPE.keys(), key=len, reverse=True)

STOP_CHARS = set("，。；：、（）()【】[]《》<>\"\"''！？!? \t\n\r\u3000")


class OrganizationDetector(DetectorBase):
    def detect(self, text: str) -> list[Hit]:
        raw = []
        for suffix in _ALL_SUFFIXES:
            subtype = _SUFFIX_TO_TYPE[suffix]
            search_from = 0
            while True:
                pos = text.find(suffix, search_from)
                if pos == -1:
                    break
                suffix_start = pos
                suffix_end = pos + len(suffix)
                i = suffix_start - 1
                while i >= 0 and suffix_start - i <= 20:
                    if text[i] in STOP_CHARS:
                        break
                    if text[i] in ("和", "与") and any(suf in text[:i+1] for suf in _ALL_SUFFIXES):
                        break
                    i -= 1
                candidate_start = i + 1
                candidate = text[candidate_start:suffix_end]
                if len(candidate) - len(suffix) < 2:
                    search_from = suffix_end
                    continue
                if any(candidate.count(suf) > 1 for suf in _ALL_SUFFIXES):
                    search_from = suffix_end
                    continue
                if candidate and candidate[0] in STOP_CHARS:
                    search_from = suffix_end
                    continue
                raw.append((candidate, subtype, len(suffix)))
                search_from = suffix_end

        # longest suffix priority + contained filter
        raw.sort(key=lambda x: (-(x[2]),))
        final = []
        for cand, subtype, suf_len in raw:
            if any(cand != other[0] and cand in other[0] for other in raw):
                continue
            if cand not in [f[0] for f in final]:
                final.append((cand, subtype))

        return [Hit(text=c, type=f"ORG_{st}") for c, st in final]





