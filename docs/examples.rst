Examples
========

Getting a Project's Dependencies
--------------------------------

`pypi_simple` can be used to fetch a project's dependencies (specifically, the
dependencies for each of the project's distribution packages) as follows.

Note that Warehouse only began storing the contents of package :file:`METADATA`
files in May 2023.  Packages uploaded prior to that point are gradually having
their metadata "backfilled" in; see
<https://github.com/pypi/warehouse/issues/8254> for updates.

.. code:: python

    # Requirements:
    #     Python 3.8+
    #     packaging 23.1+
    #     pypi_simple 1.3+

    from packaging.metadata import parse_email
    from pypi_simple import PyPISimple

    with PyPISimple() as client:
        page = client.get_project_page("pypi-simple")
        for pkg in page.packages:
            if pkg.has_metadata:
                src = client.get_package_metadata(pkg)
                md, _ = parse_email(src)
                if deps := md.get("requires_dist"):
                    print(f"Dependencies for {pkg.filename}:")
                    for d in deps:
                        print(f"    {d}")
                else:
                    print(f"Dependencies for {pkg.filename}: NONE")
            else:
                print(f"{pkg.filename}: No metadata available")
            print()


Downloading With a Rich Progress Bar
------------------------------------

The `PyPISimple.download_package()` method can be passed a callable for
constructing a progress bar to use when downloading.  `pypi_simple` has
built-in support for using a tqdm_ progress bar, but any progress bar can be
used if you provide the right structure.

Here is an example of using a progress bar from rich_.  The progress bar uses
the default settings; adding customization is left as an exercise to the
reader.

.. _tqdm: https://tqdm.github.io
.. _rich: https://github.com/Textualize/rich

.. code:: python

    from __future__ import annotations
    from dataclasses import InitVar, dataclass, field
    from types import TracebackType
    from pypi_simple import PyPISimple
    from rich.progress import Progress, TaskID

    @dataclass
    class RichProgress:
        bar: Progress = field(init=False, default_factory=Progress)
        task_id: TaskID = field(init=False)
        size: InitVar[int | None]

        def __post_init__(self, size: int | None) -> None:
            self.task_id = self.bar.add_task("Downloading...", total=size)

        def __enter__(self) -> RichProgress:
            self.bar.start()
            return self

        def __exit__(
            self,
            _exc_type: type[BaseException] | None,
            _exc_val: BaseException | None,
            _exc_tb: TracebackType | None,
        ) -> None:
            self.bar.stop()

        def update(self, increment: int) -> None:
            self.bar.update(self.task_id, advance=increment)


    with PyPISimple() as client:
        page = client.get_project_page("numpy")
        pkg = page.packages[-1]
        client.download_package(pkg, path=pkg.filename, progress=RichProgress)
