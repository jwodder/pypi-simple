from abc import ABC, abstractmethod
import hashlib
from typing import Any, Dict, Optional
from urllib.parse import urljoin
import warnings
from packaging.version import Version
from . import SUPPORTED_REPOSITORY_VERSION


def check_repo_version(
    declared_version: str,
    supported_version: str = SUPPORTED_REPOSITORY_VERSION,
) -> None:
    """
    Raise an `UnsupportedRepoVersionError` if ``declared_version`` has a
    greater major version component than ``supported_version``, or emit an
    `UnexpectedRepoVersionWarning` if ``declared_version`` has a greater minor
    version component than ``supported_version``
    """
    declared = Version(declared_version)
    supported = Version(supported_version)
    if (declared.epoch, declared.major) > (supported.epoch, supported.major):
        raise UnsupportedRepoVersionError(declared_version, supported_version)
    elif declared.minor > supported.minor:
        warnings.warn(
            f"Repository's version ({declared_version}) has greater minor"
            f" component than supported version ({supported_version})",
            UnexpectedRepoVersionWarning,
        )


class UnsupportedRepoVersionError(Exception):
    """
    Raised upon encountering a simple repository whose repository version
    (:pep:`629`) has a greater major component than the maximum supported
    repository version (`SUPPORTED_REPOSITORY_VERSION`)
    """

    def __init__(self, declared_version: str, supported_version: str) -> None:
        #: The version of the simple repository
        self.declared_version: str = declared_version
        #: The maximum repository version that we support
        self.supported_version: str = supported_version

    def __str__(self) -> str:
        return (
            f"Repository's version ({self.declared_version}) has greater major"
            f" component than supported version ({self.supported_version})"
        )


class UnexpectedRepoVersionWarning(UserWarning):
    """
    .. versionadded:: 0.10.0

    Emitted upon encountering a simple repository whose repository version
    (:pep:`629`) has a greater minor version components than the maximum
    supported repository version (`SUPPORTED_REPOSITORY_VERSION`).

    This warning can be emitted by anything that can raise
    `UnsupportedRepoVersionError`.
    """

    pass


class UnsupportedContentTypeError(ValueError):
    """
    Raised when a response from a simple repository has an unsupported
    :mailheader:`Content-Type`
    """

    def __init__(self, url: str, content_type: str) -> None:
        #: The URL that returned the response
        self.url = url
        #: The unsupported :mailheader:`Content-Type`
        self.content_type = content_type

    def __str__(self) -> str:
        return (
            f"Response from {self.url} has unsupported Content-Type"
            f" {self.content_type!r}"
        )


def basejoin(base_url: Optional[str], url: str) -> str:
    if base_url is None:
        return url
    else:
        return urljoin(base_url, url)


class AbstractDigestChecker(ABC):
    @abstractmethod
    def update(self, blob: bytes) -> None:
        ...

    @abstractmethod
    def finalize(self) -> None:
        ...


class NullDigestChecker(AbstractDigestChecker):
    def update(self, blob: bytes) -> None:
        pass

    def finalize(self) -> None:
        pass


class DigestChecker(AbstractDigestChecker):
    def __init__(self, digests: Dict[str, str]) -> None:
        self.digesters: Dict[str, Any] = {}
        self.expected: Dict[str, str] = {}
        for alg, value in digests.items():
            try:
                d = hashlib.new(alg)
            except ValueError:
                pass
            else:
                self.digesters[alg] = d
                self.expected[alg] = value
        if not self.digesters:
            raise NoDigestsError("No digests with known algorithms available")

    def update(self, blob: bytes) -> None:
        for d in self.digesters.values():
            d.update(blob)

    def finalize(self) -> None:
        for alg, d in self.digesters.items():
            actual = d.hexdigest()
            if actual != self.expected[alg]:
                raise DigestMismatchError(
                    algorithm=alg,
                    expected_digest=self.expected[alg],
                    actual_digest=actual,
                )


class NoDigestsError(ValueError):
    """
    .. versionadded:: 0.10.0

    Raised by `PyPISimple.download_package()` with ``verify=True`` when the
    given package does not have any digests with known algorithms
    """

    pass


class DigestMismatchError(ValueError):
    """
    .. versionadded:: 0.10.0

    Raised by `PyPISimple.download_package()` with ``verify=True`` when the
    digest of the downloaded file does not match the expected value
    """

    def __init__(
        self, algorithm: str, expected_digest: str, actual_digest: str
    ) -> None:
        #: The name of the digest algorithm used
        self.algorithm = algorithm
        #: The expected digest
        self.expected_digest = expected_digest
        #: The digest of the file that was actually received
        self.actual_digest = actual_digest

    def __str__(self) -> str:
        return (
            f"{self.algorithm} digest of downloaded file is"
            f" {self.actual_digest!r} instead of expected {self.expected_digest!r}"
        )
