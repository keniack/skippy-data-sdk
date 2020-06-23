import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="skippy-data", # Replace with your own username
    version="0.0.1",
    author="Cynthia Marcelino",
    author_email="keniack@gmail.com",
    description="look up data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bla/bla",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
