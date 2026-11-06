import os
import tempfile

from docx import Document

from pseudo_tool.processors.docx_proc import DocxProcessor
from pseudo_tool.manager import PseudonymManager
from pseudo_tool.detector import Detector


def _make(path, text):
    doc = Document()
    doc.add_paragraph(text)
    doc.save(path)


def test_docx_with_table():
    with tempfile.TemporaryDirectory() as td:
        inp = os.path.join(td, "in.docx")
        out = os.path.join(td, "out.docx")
        doc = Document()
        t = doc.add_table(rows=1, cols=1)
        t.rows[0].cells[0].text = "张三 13800001234"
        doc.save(inp)
        mgr = PseudonymManager(map_file=os.path.join(td, "m.enc"), key_file=os.path.join(td, "k.bin"))
        DocxProcessor().anonymize(inp, out, mgr, Detector())
        d2 = Document(out)
        cell_text = d2.tables[0].rows[0].cells[0].text
        assert "张三" not in cell_text


def test_docx_header_footer():
    with tempfile.TemporaryDirectory() as td:
        inp = os.path.join(td, "in.docx")
        out = os.path.join(td, "out.docx")
        doc = Document()
        doc.add_paragraph("body")
        doc.sections[0].header.paragraphs[0].text = "李娜"
        doc.save(inp)
        mgr = PseudonymManager(map_file=os.path.join(td, "m.enc"), key_file=os.path.join(td, "k.bin"))
        DocxProcessor().anonymize(inp, out, mgr, Detector())
        d2 = Document(out)
        header_text = d2.sections[0].header.paragraphs[0].text
        assert "李娜" not in header_text


def test_docx_empty():
    with tempfile.TemporaryDirectory() as td:
        inp = os.path.join(td, "in.docx")
        out = os.path.join(td, "out.docx")
        Document().save(inp)
        mgr = PseudonymManager(map_file=os.path.join(td, "m.enc"), key_file=os.path.join(td, "k.bin"))
        DocxProcessor().anonymize(inp, out, mgr, Detector())
        assert os.path.exists(out)


def test_docx_no_sensitive():
    with tempfile.TemporaryDirectory() as td:
        inp = os.path.join(td, "in.docx")
        out = os.path.join(td, "out.docx")
        _make(inp, "hello world")
        mgr = PseudonymManager(map_file=os.path.join(td, "m.enc"), key_file=os.path.join(td, "k.bin"))
        DocxProcessor().anonymize(inp, out, mgr, Detector())
        d2 = Document(out)
        assert d2.paragraphs[0].text == "hello world"
