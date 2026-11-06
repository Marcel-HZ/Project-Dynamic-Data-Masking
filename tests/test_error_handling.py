import os
import tempfile

import pytest

from pseudo_tool.processors.docx_proc import DocxProcessor
from pseudo_tool.processors.pdf_proc import PdfProcessor
from pseudo_tool.manager import PseudonymManager
from pseudo_tool.detector import Detector


def test_file_not_found():
    with tempfile.TemporaryDirectory() as td:
        mgr = PseudonymManager(map_file=os.path.join(td, "m.enc"), key_file=os.path.join(td, "k.bin"))
        with pytest.raises(FileNotFoundError):
            DocxProcessor().anonymize(os.path.join(td, "nope.docx"), os.path.join(td, "out.docx"), mgr, Detector())


def test_permission_error():
    with tempfile.TemporaryDirectory() as td:
        inp = os.path.join(td, "in.docx")
        from docx import Document
        Document().save(inp)
        mgr = PseudonymManager(map_file=os.path.join(td, "m.enc"), key_file=os.path.join(td, "k.bin"))
        # output dir non-writable: use a file path as directory
        bad_dir = os.path.join(td, "notadir")
        with open(bad_dir, "w") as f:
            f.write("x")
        with pytest.raises(PermissionError):
            DocxProcessor().anonymize(inp, os.path.join(bad_dir, "out.docx"), mgr, Detector())


def test_pdf_encrypted():
    import fitz
    with tempfile.TemporaryDirectory() as td:
        inp = os.path.join(td, "enc.pdf")
        doc = fitz.open()
        page = doc.new_page()
        page.insert_text((72, 72), "hello")
        doc.save(inp, encryption=fitz.PDF_ENCRYPT_AES_256, owner_pw="pw", user_pw="pw")
        doc.close()
        mgr = PseudonymManager(map_file=os.path.join(td, "m.enc"), key_file=os.path.join(td, "k.bin"))
        with pytest.raises(ValueError):
            PdfProcessor().anonymize(inp, os.path.join(td, "out.pdf"), mgr, Detector())
