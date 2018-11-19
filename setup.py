from setuptools import setup

requires = [
    'pingparsing',
    'pyramid',
    'pyramid_jinja2',
    'waitress',
    'iso8601',
    'speedtest-cli',
    'prometheus_client'
]

setup(
    name='instability',
    install_requires=requires,
)
