from .base import DetectorBase, Hit

ORG_SUFFIXES = ["有限公司", "股份有限公司", "有限责任公司", "集团", "科技公司",
                "事务所", "中心", "研究院", "银行", "支行", "分行", "医院",
                "学校", "大学", "学院"]

STOP_CHARS = set("，。；：、（）()【】[]《》<>\"\"''！？!? \t\n\r\u3000和与")


class OrganizationDetector(DetectorBase):
    def detect(self, text: str) -> list[Hit]:
        raw = []
        for suffix in ORG_SUFFIXES:
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
                    i -= 1
                candidate_start = i + 1
                candidate = text[candidate_start:suffix_end]
                if len(candidate) - len(suffix) < 2:
                    search_from = suffix_end
                    continue
                if candidate and candidate[0] in STOP_CHARS:
                    search_from = suffix_end
                    continue
                raw.append(candidate)
                search_from = suffix_end

        # keep candidates not contained in a longer one
        final = []
        for cand in raw:
            if any(cand != other and cand in other for other in raw):
                continue
            if cand not in final:
                final.append(cand)

        return [Hit(text=c, type="ORG") for c in final]

