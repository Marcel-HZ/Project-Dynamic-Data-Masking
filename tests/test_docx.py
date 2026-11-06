import os
import tempfile

from docx import Document

from pseudo_tool.processors.docx_proc import DocxProcessor
from pseudo_tool.manager import PseudonymManager
from pseudo_tool.detector import Detector


def _make_docx(path, text):
    doc = Document()
    doc.add_paragraph(text)
    doc.save(path)


def test_docx_roundtrip():
    with tempfile.TemporaryDirectory() as td:
        inp = os.path.join(td, "in.docx")
        out = os.path.join(td, "out.docx")
        back = os.path.join(td, "back.docx")
        original = "张三 13800001234 110101199001011234"
        _make_docx(inp, original)
        mgr = PseudonymManager(map_file=os.path.join(td, "m.enc"), key_file=os.path.join(td, "k.bin"))
        det = Detector()
        DocxProcessor().anonymize(inp, out, mgr, det)
        DocxProcessor().restore(out, back, mgr)
        d2 = Document(back)
        text = "\n".join(p.text for p in d2.paragraphs)
        assert text == original
