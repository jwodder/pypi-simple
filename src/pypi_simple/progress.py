from __future__ import annotations
from collections.abc import Callable
from types import TracebackType
from typing import TYPE_CHECKING, Any, Protocol, runtime_checkable

if TYPE_CHECKING:
    from typing_extensions import Self


@runtime_checkable
class ProgressTracker(Protocol):
    """
    A `typing.Protocol` for progress trackers.  A progress tracker must be
    usable as a context manager whose ``__enter__`` method performs startup &
    returns itself and whose ``__exit__`` method performs shutdown/cleanup.  In
    addition, a progress tracker must have an ``update(increment: int)`` method
    that will be called with the size of each downloaded file chunk.
    """

    def __enter__(self) -> Self: ...

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool | None: ...

    def update(self, increment: int) -> None: ...


class NullProgressTracker:
    def __enter__(self) -> NullProgressTracker:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        pass

    def update(self, increment: int) -> None:
        pass


def null_progress_tracker() -> Callable[[int | None], ProgressTracker]:
    def factory(_content_length: int | None) -> ProgressTracker:
        return NullProgressTracker()

    return factory


def tqdm_progress_factory(**kwargs: Any) -> Callable[[int | None], ProgressTracker]:
    """
    A function for displaying a progress bar with tqdm_ during a download.
    Naturally, using this requires tqdm to be installed alongside
    ``pypi-simple``.

    Call `tqdm_progress_factory()` with any arguments you wish to pass to the
    ``tqdm.tqdm`` constructor, and pass the result as the ``progress`` argument
    to `PyPISimple.download_package()`.

    .. _tqdm: https://tqdm.github.io

    Example:

    .. code:: python

        with PyPISimple() as client:
            page = client.get_project_page("pypi-simple")
            pkg = page.packages[-1]
            client.download_package(
                pkg,
                path=pkg.filename,
                progress=tqdm_progress_factory(desc="Downloading ..."),
            )
    """

    from tqdm import tqdm

    def factory(content_length: int | None) -> ProgressTracker:
        return tqdm(total=content_length, **kwargs)

    return factory
