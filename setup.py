from setuptools import find_packages, setup

with open("./README.md", "r") as f:
    long_description = f.read()

setup(
    name="Phractal",
    version="0.0.3a",
    description="A tool for creating HTML documents programmatically with Python",
    package_dir={"": "app"},
    packages=find_packages(where="app"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Hauteclere/phractal",
    author="Hauteclere",
    author_email="hauteclere.code@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "Jinja2 >= 3.1.2", 
        "MarkupSafe >=2.1.2", 
        "pydantic >= 1.10.6", 
        "typing_extensions >= 4.5.0"
    ],
    extras_require={
        "dev": ["twine>=4.0.2"],
    },
    python_requires=">=3.10",
)
