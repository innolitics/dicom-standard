# DICOM Standard Parser

This repository contains code that parses the DICOM standard into JSON files.

## Setup

You will need the following system level dependencies:

- Python 3.5.x
- Make + Unix tools

You will probably also want to setup a "virtual environment" (e.g. using Conda, or Pyenv + Virtualenv) to install the project dependencies into.  Once you are in your "virtual environment", you can run:

    make

to install and compile everything.

## Design Philosophy

- Each step in the parsing process is classified as either an "extract" stage, or a "process" stage.
- Stages are python scripts that take one or more files as inputs, and write their output to standard out.
- "Extract" stages takes a single HTML input file and print out JSON.
- "Process" stages take one or more JSON files as inputs and print out JSON.
