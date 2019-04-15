from setuptools import setup

# List of dependencies installed via `pip install -e .`
# by virtue of the Setuptools `install_requires` value below.
requires = [
    'pyramid',
    'waitress',
    'pyramid_jinja2',
#    'Wand',
    'Pillow',
]

setup(
    name='galdir',
    install_requires=requires,
    entry_points={
        'paste.app_factory': [
            'main = galdir:main'
        ],
    },
)
