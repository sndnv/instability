from setuptools import setup

requires = [
    'pingparsing',
    'pyramid',
    'pyramid_jinja2',
    'waitress',
    'iso8601',
]

setup(
    name='tutorial',
    install_requires=requires,
)
