from __future__ import annotations
from abc import ABC, abstractmethod
import hashlib
from typing import Any, Optional
from urllib.parse import urljoin
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
    def __init__(self, digests: dict[str, str]) -> None:
        self.digesters: dict[str, Any] = {}
        self.expected: dict[str, str] = {}
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
