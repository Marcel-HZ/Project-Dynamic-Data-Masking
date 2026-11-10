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
        self.org = OrganizationDetector()
        self.address = AddressDetector()
        self.name = NameDetector()

    def detect(self, text: str) -> list[Hit]:
        hits = []
        seen = set()
        id_texts = {h.text for h in self.id_card.detect(text)}
        for d in (self.id_card, self.uscc, self.phone, self.email, self.org, self.address):
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
        # ADDRESS overlap: skip if overlaps with ORG
        org_texts = {h.text for h in hits if h.type.startswith("ORG")}
        addr_hits = []
        for h in hits:
            if h.type == "ADDRESS":
                # skip if overlaps with any ORG
                if any(h.text in ot or ot in h.text for ot in org_texts):
                    continue
                addr_hits.append(h)
            else:
                addr_hits.append(h)
        hits = addr_hits
        self.name.set_overlap_provider(lambda: {h.text for h in hits})
        for h in self.name.detect(text):
            key = (h.text, h.type)
            if key in seen:
                continue
            seen.add(key)
            hits.append(h)
        return hits
