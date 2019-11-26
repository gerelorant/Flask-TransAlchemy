from setuptools import setup
from os import path


this_directory = path.abspath(path.dirname(__file__))

with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='Flask-TransAlchemy',
    version='0.1',
    packages=['flask_transalchemy'],
    url='https://github.com/gerelorant/Flask-TransAlchemy',
    license='MIT',
    author='Gere Lóránt',
    author_email='gerelorant@gmail.com',
    description='Simple translation support for '
                'Flask-SQLAlchemy based database tables.',
    install_requires=['Flask', 'Flask-SQLAlchemy', 'Flask-BabelEx'],
    include_package_data=True,
    long_description=long_description,
    long_description_content_type='text/markdown'
)
