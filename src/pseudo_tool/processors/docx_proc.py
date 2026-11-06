import os
from docx import Document

from .base import ProcessorBase
from ..utils.logger import audit
from ..utils.text import merge_runs


class DocxProcessor(ProcessorBase):
    def _iter_paragraphs(self, doc):
        for p in doc.paragraphs:
            yield p
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    for p in cell.paragraphs:
                        yield p
        for section in doc.sections:
            for p in section.header.paragraphs:
                yield p
            for p in section.footer.paragraphs:
                yield p

    def anonymize(self, inp, out, manager, detector) -> None:
        if not os.path.exists(inp):
            raise FileNotFoundError(f"输入文件不存在：{inp}")
        out_dir = os.path.dirname(os.path.abspath(out))
        if (not os.path.isdir(out_dir)) or (not os.access(out_dir, os.W_OK)):
            raise PermissionError(f"输出目录不可写：{out_dir}")
        doc = Document(inp)
        for p in self._iter_paragraphs(doc):
            merge_runs(p)
        full_text = "\n".join(p.text for p in self._iter_paragraphs(doc))
        hits = detector.detect(full_text)
        mapping = {h.text: manager.get_pseudonym(h.text, h.type) for h in hits}
        for p in self._iter_paragraphs(doc):
            for run in p.runs:
                for real, pseudo in mapping.items():
                    run.text = run.text.replace(real, pseudo)
        doc.save(out)
        from collections import Counter
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
        doc = Document(inp)
        rmap = manager.reverse_map()
        for p in self._iter_paragraphs(doc):
            for run in p.runs:
                for pseudo, real in rmap.items():
                    run.text = run.text.replace(pseudo, real)
        doc.save(out)
