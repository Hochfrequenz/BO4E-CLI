import gc

from pydantic import BaseModel, ConfigDict

from bo4e_cli.models.weakref import WeakCollection


class Dummy(BaseModel):
    model_config = ConfigDict(frozen=True)
    a: str


class TestWeakrefCollection:
    def test_collection_methods(self):
        collection = WeakCollection[Dummy]()
        dummy1_hard_ref = Dummy(a="Hello")
        dummy2_hard_ref = Dummy(a="World")
        collection.add(dummy1_hard_ref)
        assert len(collection) == 1
        assert dummy1_hard_ref in collection
        assert dummy2_hard_ref not in collection
        collection.add(dummy2_hard_ref)
        assert len(collection) == 2
        assert dummy2_hard_ref in collection
        assert set(collection) == {dummy1_hard_ref, dummy2_hard_ref}
        collection.remove(dummy2_hard_ref)
        assert len(collection) == 1
        assert dummy2_hard_ref not in collection
        assert dummy1_hard_ref in collection

    def test_gc_deletion(self):
        collection = WeakCollection[Dummy]()
        dummy1_hard_ref = Dummy(a="Hello")
        dummy2_hard_ref = Dummy(a="World")
        collection.add(dummy1_hard_ref)
        collection.add(dummy2_hard_ref)
        assert len(collection) == 2
        del dummy1_hard_ref
        gc.collect()
        assert len(collection) == 1
        assert dummy2_hard_ref in collection