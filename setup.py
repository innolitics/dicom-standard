from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
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
        'Programming Language :: Python :: 3.7',
    ],

    keywords='dicom standard json',

    packages=find_packages(exclude=['contrib', 'tests']),

    install_requires=[
        'beautifulsoup4',
        'py',
    ],

    extras_require={
        'dev': ['check-manifest'],
        'test': ['pytest'],
    },

    package_data={
        'standard': [
            'attributes.json',
            'ciod_to_fg_macros.json',
            'ciod_to_modules.json',
            'ciods.json',
            'confidentiality_profile_attributes.json',
            'macros.json',
            'macro_to_attributes.json',
            'modules.json',
            'module_to_attributes.json',
            'references.json',
            'sops.json',
        ],
    },

    data_files=[],
    entry_points={},
)
