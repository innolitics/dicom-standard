from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='dicom-standard',

    version='0.1.0',

    description='Parse the DICOM Standard into a human-friendly JSON format.',
    long_description=long_description,
    url='https://github.com/innolitics/dicom-standard',
    author='Innolitics, LLC',
    author_email='info@innolitics.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Intended Audience :: Healthcare Industry',
        'Topic :: Scientific/Engineering :: Medical Science Apps.',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    keywords='dicom standard json',

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    install_requires=[
        'beautifulsoup4',
        'py',
    ],

    extras_require={
        'dev': [],
        'test': ['pytest'],
    },

    package_data={
        'standard': [
            'ciods.json',
            'ciod_to_modules.json',
            'modules.json',
            'module_to_attributes.json',
            'attributes.json',
            'references.json',
        ],
    },

    data_files=[],
    entry_points={},
)
