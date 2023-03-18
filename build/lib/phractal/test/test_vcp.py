import unittest
from typing import Any
from src.validated_cached_property import ValidatedCachedProperty
from pydantic import ValidationError

class TestVCP(unittest.TestCase):
    def test_correct_hint_validation(self):
        
        class TestClass:
            @ValidatedCachedProperty
            def test_prop(self) -> int:
                return 1
        try:
            test_thing = TestClass()
            test_thing.test_prop
        except (ValidationError, ValueError) as e:
            self.fail("A VCP with correct type-hinting incorrectly raised an error.")

    def test_incorrect_hint_validation(self):
        class TestClass:
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
        class TestClass:
            @ValidatedCachedProperty
            def test_prop(self):
                return "hi"
        with self.assertRaises(
            ValueError,
            msg="A missing type hint did not raise a ValueError."
        ):
            test_thing = TestClass()
            test_thing.test_prop

    def test_correct_parameterized_generic(self):
        class TestClass:
            @ValidatedCachedProperty
            def test_prop(self) -> list[int]:
                return [1, 2, 3]

        try:
            test_thing = TestClass()
            test_thing.test_prop
        except (ValidationError, ValueError) as e:
            self.fail("A VCP with correct type-hinting (list[int]) incorrectly raised an error.")

    def test_union_return_type_hint(self):
        class TestClass:
            @ValidatedCachedProperty
            def test_prop(self) -> int|bool:
                return 3
            
        try:
            test_thing = TestClass()
            test_thing.test_prop
        except (ValidationError, ValueError) as e:
            self.fail("A VCP with correct type-hinting (int|bool) incorrectly raised an error.")

    def test_any_return_hint(self):
        class TestClass:
            @ValidatedCachedProperty
            def test_prop(self) -> Any:
                return 3
            
        try:
            test_thing = TestClass()
            test_thing.test_prop
        except (ValidationError, ValueError) as e:
            self.fail("A VCP with correct type-hinting (Any) incorrectly raised an error.")

    def test_incorrect_parameterized_generic(self):
        class TestClass:
            @ValidatedCachedProperty
            def test_prop(self) -> list[int]:
                return [1, "b", 3]
            
        with self.assertRaises(ValueError) as e:
            test_thing = TestClass()
            test_thing.test_prop

    def test_incorrect_union_hint(self):
        class TestClass:
            @ValidatedCachedProperty
            def test_prop(self) -> int|bool:
                return "hi"
            
        with self.assertRaises(ValueError) as e:
            test_thing = TestClass()
            test_thing.test_prop

    def test_parameterized_non_generics(self):
        class TestClass1:
            pass

        class TestClass2:
            @ValidatedCachedProperty
            def test_prop(self) -> list[TestClass1]:
                return [TestClass1(), TestClass1()]
            
        try:
            test_thing = TestClass2()
            test_thing.test_prop
        except (ValidationError, ValueError) as e:
            self.fail("A VCP with correct type-hinting (Any) incorrectly raised an error.")

    def test_incorrect_parameterized_non_generics(self):
        class TestClass1:
            pass

        class TestClass3:
            pass

        class TestClass2:
            @ValidatedCachedProperty
            def test_prop(self) -> list[TestClass1]:
                return [TestClass1(), TestClass3()]
            
        with self.assertRaises(ValueError) as e:
            test_thing = TestClass2()
            test_thing.test_prop