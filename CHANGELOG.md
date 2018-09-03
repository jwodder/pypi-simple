v0.3.0 (2018-09-03)
-------------------
- When fetching the list of files for a project, the project name is now used
  to resolve ambiguous filenames.
- The filename parser now requires all filenames to be all-ASCII (except for
  wheels).

v0.2.0 (2018-09-01)
-------------------
- The filename parser now rejects invalid project names, blatantly invalid
  versions, and non-ASCII digits.
- RPM packages are now recognized.

v0.1.0 (2018-08-31)
-------------------
Initial release
