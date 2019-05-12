v0.5.0 (2019-05-12)
-------------------
- The `PyPISimple` constructor now takes an optional `session` argument which
  can be used to specify a `requests.Session` object with more complicated
  configuration than just authentication
- Support for PEP 592; `DistributionPackage` now has a `yanked` attribute

v0.4.0 (2018-09-06)
-------------------
- Publicly (i.e., in the README) document the utility functions
- Gave `PyPISimple` an `auth` parameter for specifying login/authentication
  details

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
