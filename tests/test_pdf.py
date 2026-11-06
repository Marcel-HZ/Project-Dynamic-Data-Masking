import os
import tempfile

import fitz

from pseudo_tool.processors.pdf_proc import PdfProcessor
from pseudo_tool.manager import PseudonymManager
from pseudo_tool.detector import Detector


def _make_pdf(path, text):
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), text)
    doc.save(path)
    doc.close()


def test_pdf_anonymize():
    with tempfile.TemporaryDirectory() as td:
        inp = os.path.join(td, "in.pdf")
        out = os.path.join(td, "out.pdf")
        _make_pdf(inp, "Zhang San 13800001234")
        mgr = PseudonymManager(map_file=os.path.join(td, "m.enc"), key_file=os.path.join(td, "k.bin"))
        det = Detector()
        PdfProcessor().anonymize(inp, out, mgr, det)
        assert os.path.exists(out)
