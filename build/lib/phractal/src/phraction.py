from pydantic import BaseModel, FilePath, validator
from functools import cached_property
from jinja2 import Environment, BaseLoader, TemplateSyntaxError 
from typing import Union, AbstractSet, Mapping, Any
from .validated_cached_property import ValidatedCachedProperty

AbstractSetIntStr = Union[AbstractSet, int, str]
MappingIntStrAny = Union[Mapping, int, str, Any]
DictStrAny = Union[dict, str, Any]

class Phraction(BaseModel):
    """The base unit of construction of a Phractal document - analagous to React.Component.
    Renders a supplied template as an HTML string, automatically inserting field values.
    
    Performs Pydantic-based field validation/type-checking. 
    
    Args:
        template: A Jinja2-formatted string defining the HTML structure of the Phraction.
    """

    template: str

    class Config:
        arbitrary_types_allowed = True
        validate_assignment = True
        keep_untouched = (cached_property,)

    def __repr__(self):
        template = Environment(loader=BaseLoader).from_string(self.template)
        return template.render(self.dict())

    def __str__(self):
        return repr(self)

    def save(self, path: FilePath):
        """Writes a rendered Phraction document to file as HTML.

        Args:
            path: The local filepath to which the rendered document should be saved.        
        """
        with open(path, 'w') as output_file:
                output_file.write(repr(self))

    @validator("template", always=True)
    @classmethod
    def check_template(cls, value) -> str:
        
        if not isinstance(value, str):
            raise ValueError(f"Invalid template supplied to {cls.__name__}. Template must be a Jinja2-formatted string.")
        
        try:
            env = Environment(loader=BaseLoader)
            env.parse(value)
        except TemplateSyntaxError as e:
            raise ValueError(f"Invalid template supplied to {cls.__name__}. Error on line {e.lineno} of template.\n\tError message: {e.message}")
        return value

    @classmethod
    def get_properties(cls) -> list[str]:
        return [prop for prop in dir(cls) if isinstance(getattr(cls, prop), property) or isinstance(getattr(cls, prop), ValidatedCachedProperty)]

    def dict(
        self,
        *,
        include: Union['AbstractSetIntStr', 'MappingIntStrAny'] = None,
        exclude: Union['AbstractSetIntStr', 'MappingIntStrAny'] = None,
        by_alias: bool = False,
        skip_defaults: bool = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
    ) -> 'DictStrAny':
        """Performs identically to the Pydantic Basemodel's .dict() method, except that Properties and ValidatedCachedProperties are also included."""

        attribs = super().dict(
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            skip_defaults=skip_defaults,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none
        )
        props = self.get_properties()
        # Include and exclude properties
        if include:
            props = [prop for prop in props if prop in include]
        if exclude:
            props = [prop for prop in props if prop not in exclude]

        # Update the attribute dict with the properties
        if props:
            attribs.update({prop: getattr(self, prop) for prop in props})

        return attribs

    def with_boilerplate(self, bootstrap: bool=False, title: str="Phractal Document"):
        """A method to wrap the output of a phraction in standard HTML boilerplate. Use ONLY on the top-level Phraction in a doc.

        args:
            bootstrap: Boolean. Indicates whether or not to include Bootstrap styling script v4.3.1 in head.
            title: String. The <title> to assign in the document's head. Default is "Phractal Document".
        
        returns:
            An object of the Phraction class which wraps the calling instance in boilerplate.
        """
        class Boilerplater(Phraction):
            template = """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <meta http-equiv="X-UA-Compatible" content="ie=edge">
                {% if bootstrap %}
                    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
                {% endif %}
                <title>{{ title }}</title>
            </head>
            <body>
                {{ inner_phractal }}
            </body>
            </html>"""
            title: str
            bootstrap: bool
            
            @property
            def inner_phractal(obj):
                return self

        boilerplater=Boilerplater(
            title = title,
            bootstrap = bootstrap
        )
        
        return boilerplater
