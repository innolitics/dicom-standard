# DICOM Standard Parser

This program parses the web version of the [DICOM Standard][nema] into human
and machine-friendly JSON files. The purpose of these JSON files is twofold:

1. To provide a standardized and machine-readable way to access DICOM Standard
   information for software applications

2. To provide a logical model for the relationships between cross-referenced
   sections in the DICOM Standard

The finalized JSON output of this program is in the `standard` directory at the
top level of this project.

[nema]: http://dicom.nema.org/

## Setup

To run this program and generate the JSON files, you will need the following
system level dependencies:

- Python 3.5.x
- Make + Unix tools

You will probably also want to setup a "virtual environment" (e.g. using Conda,
or Pyenv + Virtualenv) to install the project dependencies into.  Once you are
in your "virtual environment", you can run:

    $ make

to install and compile everything. Add the `-j` flag to speed this process up
significantly.

### Updating the Standard

To download and parse the most up-to-date web version of the DICOM Standard,
run the following commands:

    $ make clean
    $ make updatestandard
    $ make

## Design Philosophy

The overall data flow of this program takes the following form:

```
          extract                      (post)process
Raw HTML ---------> JSON intermediate ---------------> JSON final

```

During this process, the following invariants are maintained:

- Each step in the parsing process is classified as either an "extract" stage,
  or a "process" stage.
- Stages are python scripts that take one or more files as inputs, and write
  their output to standard out.
- "Extract" stages takes one more more HTML input files and print out JSON.
- "Process" stages take one or more JSON files as inputs and print out JSON.

In this way, raw HTML is not touched by any stage other than `extract_*.py`,
and successive processing steps use increasingly refined JSON.

### Parser Stages

A map of all extraction and processing pathways is shown below:

```
               +-------+                  +----------+     +-------+
               | PS3.3 |                  |  Other   |     | PS3.6 |
               +---+---+                  |  DICOM   |     +----+--+
                   |                      | Sections |          |
                   |                      +-------+--+          |
                   |                              |             |
       +--------------------------+-----------+   |             |
       |           |              |           |   |             |
   +---v-----+  +--v-------+  +---v-----+  +--v---v---+  +------v-----+
   | Extract |  | Extract  |  | Extract |  | Extract  |  |  Extract   |
   | CIODs/  |  | Modules/ |  | Macros  |  | Sections |  | Attributes |
   | Modules |  |  Attrs   |  +-+-------+  +--+-------+  +----+-------+
   +-+------++  +--------+-+    |             |               |
     |      |            |   +--+             |               |
     |      |            |   |                |               |
+----v----+ |       +----v---v---+            |               |
| Process | |       | Preprocess |            |               |
|  CIODS  | |       |  Modules/  |            |               v
+----+----+ |       | Attributes |            |      attributes.json
     |      |       +--+--------++            |
     v      |          |        |             |
 ciods.json |      +---v-----+  |             |
            |      | Process |  |             |
    +-------v---+  | Modules |  |             |
    | Process   |  +-----+---+  +-+           |
    |  CIOD/    |        |        |           |
    | Attribute |        v        |           |
    | Relations |   modules.json  |           |
    +------+----+                 |           |
           |                      |           |
           v                +-----v-----+     |
     ciod_to_modules.json   |  Process  |     |
                            |  Module   |     |
                            | Attribute |     |
                            | Relations |     |
                            +-----+-----+     |
                                  |           |
                                +-+-----------+--+
                                | Post+process   |
                                | Add References |
                                +--+----------+--+
                                   |          |
                                   v          v
            module_to_attributes.json       references.json
```

## Contact

Find a bug? JSON files missing a piece of information? [We welcome pull
requests!][gh_link] Feel free to make a PR or make a GitHub issue for any bugs
you may find.

[gh_link]: https://www.github.com/innolitics/dicom-standard
