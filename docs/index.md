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

    make

to install and compile everything.

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
