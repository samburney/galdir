from setuptools import setup

# List of dependencies installed via `pip install -e .`
# by virtue of the Setuptools `install_requires` value below.
requires = [
    'flask',
    'Pillow',
]

setup(
    name='galdir',
    install_requires=requires,
)
