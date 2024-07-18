from __future__ import annotations
from abc import ABC, abstractmethod
import hashlib
from typing import Any, Optional
from urllib.parse import urljoin, urlparse, urlunparse
import warnings
from packaging.version import Version
from . import SUPPORTED_REPOSITORY_VERSION
from .errors import (
    DigestMismatchError,
    NoDigestsError,
    UnexpectedRepoVersionWarning,
    UnsupportedRepoVersionError,
)


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
            stacklevel=3,
        )


def basejoin(base_url: Optional[str], url: str) -> str:
    if base_url is None:
        return url
    else:
        return urljoin(base_url, url)


class AbstractDigestChecker(ABC):
    @abstractmethod
    def update(self, blob: bytes) -> None: ...

    @abstractmethod
    def finalize(self) -> None: ...


class NullDigestChecker(AbstractDigestChecker):
    def update(self, blob: bytes) -> None:
        pass

    def finalize(self) -> None:
        pass


class DigestChecker(AbstractDigestChecker):
    def __init__(self, digests: dict[str, str], url: str) -> None:
        self.digesters: dict[str, Any] = {}
        self.expected: dict[str, str] = {}
        self.url = url
        for alg, value in digests.items():
            try:
                d = hashlib.new(alg)
            except ValueError:
                pass
            else:
                self.digesters[alg] = d
                self.expected[alg] = value
        if not self.digesters:
            raise NoDigestsError(self.url)

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
                    url=self.url,
                )


def url_add_suffix(url: str, suffix: str) -> str:
    """
    Append `suffix` to the path portion of the URL `url`.  Any query parameters
    or fragments on the URL are discarded.
    """
    u = urlparse(url)
    return urlunparse((u[0], u[1], u[2] + suffix, "", "", ""))
