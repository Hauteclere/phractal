import unittest
from src.phraction import Phraction
from src.validated_cached_property import ValidatedCachedProperty
from pydantic import ValidationError

class TestTemplate(unittest.TestCase):
    def test_correct_template_validation(self):
        try:
            class GoodPhraction(Phraction):
                template = "<p>{{ msg }}</p>"
            hi = GoodPhraction()
        except ValidationError as e:
            self.fail("A Phraction with a correct template raised a validation error.")

    def test_incorrect_template_validation(self):
        with self.assertRaises(
            ValidationError, 
            msg="A malformed template was provided but no exception was raised."
        ):
            class BadPhraction(Phraction):
                template = "<p>{{ msg }</p>"
                msg: str

            hi = BadPhraction(msg="hi")

class TestRender(unittest.TestCase):
    def test_blank_template_render(self):
        class SomePhraction(Phraction):
            template = "<p>hi</p>"
        hi = SomePhraction()
        self.assertEqual(str(hi), "<p>hi</p>")

    def test_template_variable_render(self):
        class SomePhraction(Phraction):
            template = "<p>{{ somevar }}</p>"
            somevar: str
        hi = SomePhraction(somevar="hi")
        self.assertEqual(str(hi), "<p>hi</p>")

class TestValidation(unittest.TestCase):
    def test_validate_incorrect_type_variable(self):
        class SomePhraction(Phraction):
            template = "<p>{{ somevar }}</p>"
            somevar: int
        
        with self.assertRaises(
            ValidationError, 
            msg="Incorrect type did not raise a ValidationError."
        ):
            hi = SomePhraction(somevar="hi")

    def test_validate_correct_type_variable(self):
        class SomePhraction(Phraction):
            template = "<p>{{ somevar }}</p>"
            somevar: int
        
        try:
            hi = SomePhraction(somevar=1)
        except ValidationError as e:
            self.fail("Correctly-typed variable raised a validation error.")

class TestProperties(unittest.TestCase):
    def test_properties_included_in_render(self):
        class SomePhraction(Phraction):
            template = "<p>{{ somevar }}</p>"

            @property
            def somevar(self):
                return "hi"
            
        self.assertEqual(str(SomePhraction()), "<p>hi</p>")

    def test_validated_cached_properties_included_in_render(self):
        class SomePhraction(Phraction):
            template = "<p>{{ somevar }}</p>"

            @ValidatedCachedProperty
            def somevar(self) -> str:
                return "hi"
            
        self.assertEqual(str(SomePhraction()), "<p>hi</p>")

class TestNesting(unittest.TestCase):
    def test_nesting(self):
        class FirstPhrac(Phraction):
            template = "{{ some_var }}"
            some_var: str

        class SecondPhrac(Phraction):
            template = "<p>{{ first_phrac }}</p>"
            some_var: str

            @property
            def first_phrac(self):
                return FirstPhrac(some_var=self.some_var)
            
        test_phrac = SecondPhrac(some_var="hi")
        
        self.assertEqual(str(test_phrac), "<p>hi</p>")

class TestIntentionalFail(unittest.TestCase):
    def test_fail(self):
        self.fail()