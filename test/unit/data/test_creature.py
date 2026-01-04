import os
import pytest
from model.creature import Creature
from error import Missing, Duplicate

# set this before data imports below for data.init:
os.environ["CRYPTID_SQLITE_DB"] = ":memory:"
from data import creature


@pytest.fixture
def sample() -> Creature:
    return Creature(
        name="Yeti",
        country="CN",
        description="Hirsute Himalayan",
        aka="Abominable Snowman",
        area="*",
    )


def test_create(sample: Creature):
    resp = creature.create(sample)
    assert resp == sample


def test_create_duplicate(sample):
    with pytest.raises(Duplicate):
        creature.create(sample)


def test_get_one(sample):
    resp = creature.get_one(sample.name)
    assert resp == sample


def test_get_one_missing():
    with pytest.raises(Missing):
        creature.get_one("boxturtle")


def test_modify(sample):
    sample.area = "hehehe"
    resp = creature.modify(sample.name, sample)
    assert resp == sample


def test_modify_missing():
    thing = Creature(
        name="snurfle", country="ru", area="xxx", description="some thing", aka="..."
    )
    with pytest.raises(Missing):
        creature.modify(thing.name, thing)


def test_delete(sample):
    resp = creature.delete(sample.name)
    assert resp is None


def test_delete_missing(sample):
    with pytest.raises(Missing):
        creature.delete(sample.name)
