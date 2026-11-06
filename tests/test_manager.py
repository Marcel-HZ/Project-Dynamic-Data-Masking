from pathlib import Path

import pytest

from pseudo_tool.crypto_store import CryptoStore
from pseudo_tool.manager import PseudonymManager


def test_crypto_roundtrip(tmp_path):
    map_file = tmp_path / "mapping.enc"
    key_file = tmp_path / "key.bin"
    store = CryptoStore(map_file, key_file)
    data = {"forward": {"a": "b"}, "reverse": {"b": "a"}, "counters": {"NAME": 1}}
    store.save(data)
    assert store.load() == data
    store.destroy()
    assert not map_file.exists()
    assert not key_file.exists()

def test_idempotent(tmp_path):
    m = PseudonymManager(map_file=tmp_path / "m.enc", key_file=tmp_path / "k.bin")
    a = m.get_pseudonym("张三", "NAME")
    b = m.get_pseudonym("张三", "NAME")
    assert a == b
    assert a.startswith("张某")


def test_no_collision(tmp_path):
    m = PseudonymManager(map_file=tmp_path / "m.enc", key_file=tmp_path / "k.bin")
    # force a pseudo equal to a real already stored by pre-seeding counters? Instead just check uniqueness
    names = ["张三", "李四", "王五"]
    pseudos = [m.get_pseudonym(n, "NAME") for n in names]
    assert len(set(pseudos)) == len(pseudos)


def test_clear(tmp_path):
    m = PseudonymManager(map_file=tmp_path / "m.enc", key_file=tmp_path / "k.bin")
    m.get_pseudonym("张三", "NAME")
    m.save()
    assert (tmp_path / "m.enc").exists()
    m.clear()
    assert not (tmp_path / "m.enc").exists()
    assert not (tmp_path / "k.bin").exists()
    assert m.forward == {}


def test_pseudonym_compound_surname(tmp_path):
    m = PseudonymManager(map_file=tmp_path / "m.enc", key_file=tmp_path / "k.bin")
    assert m.get_pseudonym("欧阳明", "NAME").startswith("欧阳")
    assert m.get_pseudonym("司马光", "NAME").startswith("司马")
    p = m.get_pseudonym("张三", "NAME")
    assert p.startswith("张") and not any(p.startswith(cs) for cs in ["欧阳", "司马"])
