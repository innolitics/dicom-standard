# Security Policy

## Reporting a vulnerability

Please report security issues privately rather than in a public issue.

Use GitHub's private vulnerability reporting: the **Report a vulnerability** button on
the [Security tab](https://github.com/innolitics/dicom-standard/security/advisories/new).
That opens a thread visible only to the maintainers and the reporter.

Please don't test against the live site. If a proof of concept would change server state,
describe it rather than running it, or reproduce it locally. The published bundles ship
source maps, so the browser can be checked offline.

## Scope

This repository publishes the DICOM Standard as JSON, and that data backs the DICOM
Standard Browser at <https://dicom.innolitics.com>. Reports for either belong here:

- **This repository**: the Python parsing code and the generated `standard/*.json`.
- **The hosted browser**, including the File Editor, which already sends its bug reports
  to this tracker.

Out of scope: values that are parsed faithfully from the Standard but look wrong. Those
are ordinary issues, and a defect in the Standard itself needs a Correction Proposal to
NEMA.

## What to include

Where the problem is, how to reproduce it, and what it would let someone do. A minimal
reproduction is more useful than a long report.
