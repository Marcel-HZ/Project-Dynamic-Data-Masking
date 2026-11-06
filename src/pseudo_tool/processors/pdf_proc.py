import os
import fitz
from collections import Counter
from ..utils.logger import audit

from .base import ProcessorBase


class PdfProcessor(ProcessorBase):
    def anonymize(self, inp, out, manager, detector) -> None:
        if not os.path.exists(inp):
            raise FileNotFoundError(f"输入文件不存在：{inp}")
        out_dir = os.path.dirname(os.path.abspath(out))
        if (not os.path.isdir(out_dir)) or (not os.access(out_dir, os.W_OK)):
            raise PermissionError(f"输出目录不可写：{out_dir}")
        doc = fitz.open(inp)
        if doc.is_encrypted:
            raise ValueError("PDF 已加密，请先解密")
        full_text = ""
        for page in doc:
            full_text += page.get_text()
        hits = detector.detect(full_text)
        mapping = {h.text: manager.get_pseudonym(h.text, h.type) for h in hits}
        for page in doc:
            for real, pseudo in mapping.items():
                for rect in page.search_for(real):
                    page.add_redact_annot(rect, text=pseudo, fontsize=10)
            page.apply_redactions()
        doc.save(out, garbage=4, deflate=True)
        doc.close()
        cnt = Counter(h.type for h in hits)
        for kind, n in cnt.items():
            audit('anonymize', kind, n)
        manager.save()

    def restore(self, inp, out, manager) -> None:
        if not os.path.exists(inp):
            raise FileNotFoundError(f"输入文件不存在：{inp}")
        out_dir = os.path.dirname(os.path.abspath(out))
        if (not os.path.isdir(out_dir)) or (not os.access(out_dir, os.W_OK)):
            raise PermissionError(f"输出目录不可写：{out_dir}")
        doc = fitz.open(inp)
        if doc.is_encrypted:
            raise ValueError("PDF 已加密，请先解密")
        rmap = manager.reverse_map()
        for page in doc:
            for pseudo, real in rmap.items():
                for rect in page.search_for(pseudo):
                    page.add_redact_annot(rect, text=real, fontsize=10)
            page.apply_redactions()
        doc.save(out, garbage=4, deflate=True)
        doc.close()
