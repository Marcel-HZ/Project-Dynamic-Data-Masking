from pathlib import Path
from datetime import datetime

from ..config import DATA_DIR


def audit(op, kind, count):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    log_file = DATA_DIR / 'audit.log'
    with log_file.open('a', encoding='utf-8') as f:
        f.write(f'{datetime.now().isoformat()} op={op} kind={kind} count={count}\n')

