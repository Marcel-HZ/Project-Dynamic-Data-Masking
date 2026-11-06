from .detectors.base import Hit
from .detectors.id_card import IdCardDetector, UnifiedSocialCreditCodeDetector
from .detectors.phone import PhoneDetector
from .detectors.email import EmailDetector
from .detectors.address import AddressDetector
from .detectors.organization import OrganizationDetector
from .detectors.name import NameDetector

class Detector:
    def __init__(self):
        self.id_card = IdCardDetector()
        self.uscc = UnifiedSocialCreditCodeDetector()
        self.phone = PhoneDetector()
        self.email = EmailDetector()
        self.address = AddressDetector()
        self.org = OrganizationDetector()
        self.name = NameDetector()

    def detect(self, text: str) -> list[Hit]:
        hits = []
        seen = set()
        id_texts = {h.text for h in self.id_card.detect(text)}
        for d in (self.id_card, self.uscc, self.phone, self.email, self.address, self.org):
            for h in d.detect(text):
                if h.type == "USCC" and h.text in id_texts:
                    continue
                if h.type == "USCC" and h.text.isdigit():
                    continue
                key = (h.text, h.type)
                if key in seen:
                    continue
                seen.add(key)
                hits.append(h)
        self.name.set_overlap_provider(lambda: {h.text for h in hits})
        for h in self.name.detect(text):
            key = (h.text, h.type)
            if key in seen:
                continue
            seen.add(key)
            hits.append(h)
        return hits
