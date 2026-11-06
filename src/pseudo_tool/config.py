from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[2] / "data"
MAP_FILE = DATA_DIR / "mapping.enc"
KEY_FILE = DATA_DIR / "key.bin"

SUPPORTED_DOCX = {".docx"}
SUPPORTED_PDF  = {".pdf"}

PSEUDO_TEMPLATES = {
    "NAME":  "张某{n}",
    "ID":    "11010119900101{n:04d}",
    "PHONE": "1380000{n:04d}",
    "EMAIL": "user{n}@example.com",
    "ADDRESS": "某市某区某路{n}号",
    "ORG": "某公司{n}",
    "USCC": "91110000MA0000000{n:02d}",
}

SURNAMES = set(
    "赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨朱秦尤许何吕施张孔曹严华金魏陶姜戚谢邹喻柏水窦章云苏潘葛奚范彭郎鲁韦昌马苗凤花方俞任袁柳酆鲍史唐"
    "覃冼翟禤郗昝缑亢逯乜逄郄佴邝郏郓邺郦郢郯郇郐"
)
COMPOUND_SURNAMES = {"欧阳","司马","上官","诸葛","东方","皇甫","尉迟","公孙","慕容","长孙","宇文","司徒","司空","端木","南宫","独孤","夏侯","令狐","钟离","闾丘","公冶","申屠","太史","仲孙","轩辕","拓跋","呼延","鲜于","闾","亓官"}
NAME_TAIL_CHARS = set("三四五六七八九十百千万" + "伟芳娜敏静丽强磊洋艳勇军杰娟涛明超秀霞平刚桂文辉力玲婷浩宇轩然琪涵晨欣悦嘉怡思雨梦佳子博雅志建海鹏飞龙凤春秋冬雪梅兰竹菊松柏山河江湖云天星月光亮新正大小中和安康健福禄寿喜财宝玉石铁木水火土风雷电")

