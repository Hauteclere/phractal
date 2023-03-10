# Phractal

Phractal is a tool for creating documents programmatically with Python, powered by [`Pydantic`](https://docs.pydantic.dev/) and [`Jinja2`](https://jinja.palletsprojects.com/en/3.1.x/). 

Phractal solves the complexity that can arise when templating complex documents in Python by using *nesting*. Hence the name; a Phractal document is a fractal arrangement of simple components nested inside one another. Phractal is inspired by `React.js`'s component-driven development style, with the additional utility of Pydantic-enforced type-checking before the page is rendered, making debugging a breeze!

In addition to building your own pages from the ground up, any package that produces HTML output can be integrated into your Phractal documents. For example, Plotly graphs can be inserted into your components with just a few lines of code.

Phractal was originally designed to automatically generate bespoke templated statistical reports in the style of [`pandas-profiling`](https://pypi.org/project/pandas-profiling/). This is just the tip of the iceberg, though: anywhere you need to generate a document programmatically, Phractal is useful. Try creating invoices with it!

- [Phractal](#phractal)
  - [Key Features](#key-features)
    - [`phractal.Phraction`](#phractalphraction)
      - [Args:](#args)
      - [Methods:](#methods)
      - [Example:](#example)
    - [`phractal.ValidatedCachedProperty`](#phractalvalidatedcachedproperty)
      - [Example 1:](#example-1)
      - [Example 2 (nesting):](#example-2-nesting)
  - [Incorporating Other Packages](#incorporating-other-packages)
    - [Example:](#example-1)


---

## Key Features

There are two main tools that Practal makes available for document building:

[`phractal.Phraction`](#phractalphraction)

[`phractal.ValidatedCachedProperty`](#phractalvalidatedcachedproperty)

In the simple examples below, Phractal is barely more efficient than basic Jinja templating. The more complex your documents become, the more Phractal can help.


### `phractal.Phraction`
The base unit of construction of a Phractal document - analagous to `React.Component`.
- Renders a supplied template as an HTML string, automatically inserting its field values into the template where they are referenced.
- Performs Pydantic-based field validation/type-checking. 

#### Args:
- `template`: A Jinja2-formatted string defining the HTML structure of the Phraction.

#### Methods:
- `save(path: str)`: Save the rendered document to the specified filepath.

#### Example:

```python
from phractal import Phraction

# A Phraction to render a simple "hello" message
class HelloPara(Phraction):
    template = "<p>Hello {{ name }}</p>"
    name: str 

# Creating an instance of the Phraction
hello_para = HelloPara(name="Murderbot")

# Practions can be rendered to HTML strings using their __str__ method.
print(hello_para)

# Alternatively we can save to file
#   (We recommend including the usual HTML boilerplate like a <head>
#   in your document in this case; this is just an example)
# hello_para.save("./hello_para.html")
```

Output:  

```
<p>Hello Murderbot</p>
```

---

### `phractal.ValidatedCachedProperty`

A decorator that turns a method on a class into a property which is cached and validated at time of first access, and inserted into the template where its name is referenced. **Note that this can be used to nest Phractions!**
    
- Validation is based on return type hints (type hints are compulsory).
- Does not currently support parameterised generics (ex: `list[int]` is not a valid type hint; use `list` instead) -> *This is an open issue!*
- Value is calculated and cached at first access.
- `phractal.ValidatedCachedProperty` is subclassed from the inbuilt `functools.cached_property`.
- To avoid caching and validation, use the built-in `@property` decorator.

#### Example 1:

```python
from phractal import Phraction, ValidatedCachedProperty

# A Phraction to display calculated total prices with tax
class TaxBox(Phraction):
    template = '''
        <p>
            Gross: {{ "$%.2f"|format(gross_amount) }}
            Total (incl. tax): {{ "$%.2f"|format(total_amount) }}
        </p>
    '''
    gross_amount: float

    @ValidatedCachedProperty
    def total_amount(self):
        return self.gross_amount*1.1

# Creating an instance of the Phraction
my_taxbox = TaxBox(gross_amount=1000)

# Rendering to the console as an HTML string using __str__
print(my_taxbox)
```

Output: 

```
<p>
    Gross: $1000.00
    Total (incl. tax): $1100.00
</p>
```

#### Example 2 (nesting):

```python
from phractal import Phraction, ValidatedCachedProperty

# Phraction to render a simple "hello" message as an H1 heading
class HelloHeading(Phraction):
    template = "<h1>Hello {{ name }}</h1>"
    name: str 

# A Phraction to render a list item
class ClientItem(Phraction):
    template = "<li>{{ client_name }}</li>"
    client_name: str

# A Phraction to contain the heading and the list items as nested components
class HelloDiv(Phraction):
    template = '''
        <div>
            {{ hello_para }}
            Here's a list of clients:
            <ol>
                {% for client_item in clients %}
                    {{ client_item }}
                {% endfor %}
            </ol>
        </div>
    '''

    name: str
    client_names: list[str]
    
    # Validated and cached (calculated at access-time)
    @ValidatedCachedProperty
    def hello_para(self) -> HelloPara: 
        return HelloPara(name=self.name)
    
    # Neither validated nor cached.
    @property
    def clients(self):
        return [
            ClientItem(
                client_name=client_name
            ) for client_name in self.client_names
        ]

# Creating an instance of the top-level/parent Phraction
#   (No need to create instances for the nested Phractions;
#   the parent Phraction does this for us when it is rendered)
my_div = HelloDiv(
    name="Murderbot",
    client_names=[
        "Dr. Mensah",
        "Dr. Arada",
        "Dr. Ratthi",
        "Dr. Bharadwaj"
    ]
)

# Rendering to the console with __str__
print(my_div)
```

Output:

```
<div>
    <h1>Hello Murderbot</h1>
    <p>Here's a list of clients:</p>
    <ol>
        <li>Dr. Mensah</li>
        <li>Dr. Arada</li>
        <li>Dr. Ratthi</li>
        <li>Dr. Bharadwaj</li>
    </ol>
</div>
```

---

## Incorporating Other Packages

To incorporate output from other packages that generate document assets, simply incorporate these outputs into your `Phraction`s using `@Property` or `@ValidatedCachedProperty`. 

### Example:

Here we incorporate a `Plotly` Gauge Plot.

```python
from phractal import Phraction, ValidatedCachedProperty
from pydantic import Field
import plotly.graph_objects as go
import plotly.offline

# A Phraction that renders a gauge plot
class GaugePlot(Phraction):
    template = """
        <div style="width: 700px; height: 400px;">
            {{ gauge }}
        </div>
    """
        
    label: str
    numerator: int = Field(ge=0)

    # This works because plotly.offline.plot returns the plot as an HTML string 
    #   when the output_type='div' kwarg is supplied.
    @ValidatedCachedProperty
    def gauge(self) -> str:
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = self.numerator/100,
            number = { "valueformat": "%" },
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': self.label},
            gauge = {
                'axis': {'range': [None, 1]},
            },
        ))
        return plotly.offline.plot(
            fig, 
            include_plotlyjs=False, 
            output_type='div'
        )

# A parent Phraction to combine three GaugePlot Phractions under a heading
class AcademicPerformance(Phraction):
    # Plotly wants us to include plotly-latest.min.js to render the plot
    #   We can also incorporate Bootstrap styling
    #   The best place for both of these is here in the top-level Phraction.
    template = """
    <!DOCTYPE html>
        <html>
        <head>
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
        </head>
        <body>
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script> 
            <h1>Academic Performance</h1>
            {% for plot in plots %}
                {{ plot }}
            {% endfor %}
        </body>
    </html>    
    """
    
    grades: list[tuple]

    # Nesting those gauge plots
    @ValidatedCachedProperty
    def plots(self) -> list:
        return [
            GaugePlot(
                label=label, 
                numerator=numerator
            ) for (label, numerator) in self.grades
        ]

# Data to feed to the instance
grades = [
    ("English", 82), 
    ("Art", 64), 
    ("History", 79)
]

# Creating the instance
academic_performance = AcademicPerformance(grades=grades)

# The output here is a bit longer
# Let's save it to file instead of printing to console
academic_performance.save("./test.html")
```

Output:

![A series of gauge graphs rendered in an HTML Document](https://raw.github.com/hauteclere/phractal/main/readme_img/example_plotly.png)