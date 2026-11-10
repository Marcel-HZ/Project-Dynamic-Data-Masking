from .base import DetectorBase, Hit
from ..config import ORG_SUFFIX_MAP, ORG_WHITELIST

# build flat suffix -> subtype, longest first
_SUFFIX_TO_TYPE = {}
for subtype, suffixes in ORG_SUFFIX_MAP.items():
    for suf in suffixes:
        _SUFFIX_TO_TYPE[suf] = subtype
_ALL_SUFFIXES = sorted(_SUFFIX_TO_TYPE.keys(), key=len, reverse=True)

# Core org suffixes that typically indicate org names (not administrative divisions)
_CORE_ORG_SUFFIXES = set(['公司', '集团', '有限公司', '有限责任公司', '股份有限公司', '事务所', '工作室', '门市部',
    '营业部', '分公司', '子公司', '中心', '研究院', '研究所', '研究中心', '实验室', '科学院',
    '医院', '卫生院', '诊所', '保健院', '医疗中心',
    '大学', '学院', '学校', '中学', '小学', '幼儿园', '职业学院', '职业技术学院',
    '银行', '支行', '分行', '信用社', '储蓄所',
    '联合会', '协会', '学会', '基金会',
    '局', '委员会', '法工委', '办公室', '办公厅', '办事处', '派出所', '管理局', '监督局',
    '人民政府', '人民法院', '人民检察院', '公安局', '法院', '检察院', '法工委', '人大', '政协'])

STOP_CHARS = set('，。；：、那些()【】[]《》<>\"\"''那些！？!? \t\n\r\u3000盖有')


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
                    # Check special '和'/'与' logic: stop at connector only if text immediately before it
                    # ends with a core org suffix (indicating "OrgA 和 OrgB" pattern), not if "和" is inside an org name
                    if text[i] in ('和', '与'):
                        # Look back from connector to see if preceding text ends with core org suffix
                        j = i - 1
                        while j >= 0 and text[j] not in STOP_CHARS and i - j <= 10:
                            j -= 1
                        before_connector = text[j+1:i]
                        if any(before_connector.endswith(suf) for suf in _CORE_ORG_SUFFIXES):
                            break
                    if text[i] in STOP_CHARS:
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

        # skip whitelisted orgs (check if candidate ends with whitelisted term)
        def is_whitelisted(cand):
            return any(cand == w or cand.endswith(w) for w in ORG_WHITELIST)
        final = [(c, st) for c, st in final if not is_whitelisted(c)]
        # strip leading/trailing quote characters
        final = [(c.strip('\"“”'), st) for c, st in final]

        return [Hit(text=c, type=f'ORG_{st}') for c, st in final]