import unittest
from src.validated_cached_property import ValidatedCachedProperty
from pydantic import ValidationError

class TestVCP(unittest.TestCase):
    def test_correct_hint_validation(self):
        class TestClass(unittest.TestCase):
            @ValidatedCachedProperty
            def test_prop(self) -> int:
                return 1
        try:
            test_thing = TestClass()
            test_thing.test_prop
        except ValidationError as e:
            self.fail("A VCP with correct type-hinting incorrectly raised a ValidationError.")

    def test_incorrect_hint_validation(self):
        class TestClass(unittest.TestCase):
            @ValidatedCachedProperty
            def test_prop(self) -> int:
                return "hi"
        with self.assertRaises(
            ValueError,
            msg="An incorrectly typed type hint did not raise a ValueError."
        ):
            test_thing = TestClass()
            test_thing.test_prop
        
    def test_no_type_hint(self):
        class TestClass(unittest.TestCase):
            @ValidatedCachedProperty
            def test_prop(self):
                return "hi"
        with self.assertRaises(
            ValueError,
            msg="A missing type hint did not raise a ValueError."
        ):
            test_thing = TestClass()
            test_thing.test_prop