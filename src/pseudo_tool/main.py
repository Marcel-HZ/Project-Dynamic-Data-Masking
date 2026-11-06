import argparse
import os
import sys

from .config import SUPPORTED_DOCX, SUPPORTED_PDF
from .manager import PseudonymManager
from .detector import Detector
from .processors.docx_proc import DocxProcessor
from .processors.pdf_proc import PdfProcessor


def _processor(path):
    ext = os.path.splitext(path)[1].lower()
    if ext in SUPPORTED_DOCX:
        return DocxProcessor()
    if ext in SUPPORTED_PDF:
        return PdfProcessor()
    sys.exit("仅支持 .docx / .pdf")


def cmd_anonymize(args):
    proc = _processor(args.input)
    mgr = PseudonymManager()
    det = Detector()
    proc.anonymize(args.input, args.output, mgr, det)


def cmd_restore(args):
    proc = _processor(args.input)
    mgr = PseudonymManager()
    proc.restore(args.input, args.output, mgr)


def cmd_clear(args):
    PseudonymManager().clear()


def main():
    parser = argparse.ArgumentParser(prog="pseudo-tool")
    sub = parser.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("anonymize")
    a.add_argument("input")
    a.add_argument("output")
    a.set_defaults(func=cmd_anonymize)
    r = sub.add_parser("restore")
    r.add_argument("input")
    r.add_argument("output")
    r.set_defaults(func=cmd_restore)
    c = sub.add_parser("clear")
    c.set_defaults(func=cmd_clear)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
