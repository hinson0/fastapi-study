import os
import pytest
from model.explorer import Explorer
from error import Missing, Duplicate

# set this before data imports below for data.init:
os.environ["CRYPTID_SQLITE_DB"] = ":memory:"
from data import explorer


@pytest.fixture
def sample() -> Explorer:
    return Explorer(name="Alice", country="US", description="Adventurous explorer")


def test_create(sample: Explorer):
    resp = explorer.create(sample)
    assert resp == sample


def test_create_duplicate(sample):
    with pytest.raises(Duplicate):
        explorer.create(sample)


def test_get_one(sample):
    resp = explorer.get_one(sample.name)
    assert resp == sample


def test_get_one_missing():
    with pytest.raises(Missing):
        explorer.get_one("nonexistent")


def test_modify(sample):
    sample.description = "Updated description"
    resp = explorer.modify(sample.name, sample)
    assert resp == sample


def test_modify_missing():
    thing = Explorer(name="bob", country="UK", description="another explorer")
    with pytest.raises(Missing):
        explorer.modify(thing.name, thing)


def test_delete(sample):
    resp = explorer.delete(sample.name)
    assert resp is None


def test_delete_missing(sample):
    with pytest.raises(Missing):
        explorer.delete(sample.name)
