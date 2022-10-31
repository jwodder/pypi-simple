from __future__ import annotations
from typing import Optional
import pytest
from pypi_simple import DistributionPackage, Link


@pytest.mark.parametrize("fragment", ["", "#", "#sha256", "#sha256="])
def test_from_link_no_digests(fragment: str) -> None:
    pkg = DistributionPackage.from_link(
        Link(
            text="qypi-0.1.0-py3-none-any.whl",
            url=f"https://files.pythonhosted.org/packages/82/fc/9e25534641d7f63be93079bc07fa92bab136ddf5d4181059a1308a346f96/qypi-0.1.0-py3-none-any.whl{fragment}",
            attrs={},
        )
    )
    assert (
        pkg.url
        == "https://files.pythonhosted.org/packages/82/fc/9e25534641d7f63be93079bc07fa92bab136ddf5d4181059a1308a346f96/qypi-0.1.0-py3-none-any.whl"
    )
    assert pkg.digests == {}


def test_from_link_digests() -> None:
    pkg = DistributionPackage.from_link(
        Link(
            text="qypi-0.1.0-py3-none-any.whl",
            url="https://files.pythonhosted.org/packages/82/fc/9e25534641d7f63be93079bc07fa92bab136ddf5d4181059a1308a346f96/qypi-0.1.0-py3-none-any.whl#sha256=da69d28dcd527c0e372b3fa7b92fc333b327f8470175f035abc4e351b539189f",
            attrs={},
        )
    )
    assert (
        pkg.url
        == "https://files.pythonhosted.org/packages/82/fc/9e25534641d7f63be93079bc07fa92bab136ddf5d4181059a1308a346f96/qypi-0.1.0-py3-none-any.whl"
    )
    assert pkg.digests == {
        "sha256": "da69d28dcd527c0e372b3fa7b92fc333b327f8470175f035abc4e351b539189f"
    }


@pytest.mark.parametrize("has_sig", [True, False])
def test_get_sig_url(has_sig: bool) -> None:
    pkg = DistributionPackage(
        filename="qypi-0.1.0-py3-none-any.whl",
        project="qypi",
        version="0.1.0",
        package_type="wheel",
        url="https://files.pythonhosted.org/packages/82/fc/9e25534641d7f63be93079bc07fa92bab136ddf5d4181059a1308a346f96/qypi-0.1.0-py3-none-any.whl",
        digests={
            "sha256": "da69d28dcd527c0e372b3fa7b92fc333b327f8470175f035abc4e351b539189f"
        },
        requires_python=None,
        has_sig=has_sig,
        is_yanked=False,
        yanked_reason=None,
        metadata_digests=None,
        has_metadata=None,
    )
    assert (
        pkg.sig_url
        == "https://files.pythonhosted.org/packages/82/fc/9e25534641d7f63be93079bc07fa92bab136ddf5d4181059a1308a346f96/qypi-0.1.0-py3-none-any.whl.asc"
    )


@pytest.mark.parametrize(
    "link,distpkg",
    [
        (
            Link(
                text="qypi-0.1.0-py3-none-any.whl",
                url="https://files.pythonhosted.org/packages/82/fc/9e25534641d7f63be93079bc07fa92bab136ddf5d4181059a1308a346f96/qypi-0.1.0-py3-none-any.whl#sha256=da69d28dcd527c0e372b3fa7b92fc333b327f8470175f035abc4e351b539189f",
                attrs={},
            ),
            DistributionPackage(
                filename="qypi-0.1.0-py3-none-any.whl",
                url="https://files.pythonhosted.org/packages/82/fc/9e25534641d7f63be93079bc07fa92bab136ddf5d4181059a1308a346f96/qypi-0.1.0-py3-none-any.whl",
                digests={
                    "sha256": "da69d28dcd527c0e372b3fa7b92fc333b327f8470175f035abc4e351b539189f"
                },
                has_sig=None,
                requires_python=None,
                project="qypi",
                version="0.1.0",
                package_type="wheel",
                is_yanked=False,
                yanked_reason=None,
                metadata_digests=None,
                has_metadata=False,
            ),
        ),
        (
            Link(
                text="qypi-0.1.0-py3-none-any.whl",
                url="https://files.pythonhosted.org/packages/82/fc/9e25534641d7f63be93079bc07fa92bab136ddf5d4181059a1308a346f96/qypi-0.1.0-py3-none-any.whl#sha256=da69d28dcd527c0e372b3fa7b92fc333b327f8470175f035abc4e351b539189f",
                attrs={
                    "data-requires-python": "~= 3.6",
                    "data-gpg-sig": "true",
                    "data-dist-info-metadata": "sha256=ae718719df4708f329d58ca4d5390c1206c4222ef7e62a3aa9844397c63de28b",
                    "data-yanked": "Oopsy.",
                },
            ),
            DistributionPackage(
                filename="qypi-0.1.0-py3-none-any.whl",
                url="https://files.pythonhosted.org/packages/82/fc/9e25534641d7f63be93079bc07fa92bab136ddf5d4181059a1308a346f96/qypi-0.1.0-py3-none-any.whl",
                digests={
                    "sha256": "da69d28dcd527c0e372b3fa7b92fc333b327f8470175f035abc4e351b539189f"
                },
                has_sig=True,
                requires_python="~= 3.6",
                project="qypi",
                version="0.1.0",
                package_type="wheel",
                is_yanked=True,
                yanked_reason="Oopsy.",
                metadata_digests={
                    "sha256": "ae718719df4708f329d58ca4d5390c1206c4222ef7e62a3aa9844397c63de28b"
                },
                has_metadata=True,
            ),
        ),
        (
            Link(
                text="qypi-0.1.0-py3-none-any.whl",
                url="https://files.pythonhosted.org/packages/82/fc/9e25534641d7f63be93079bc07fa92bab136ddf5d4181059a1308a346f96/qypi-0.1.0-py3-none-any.whl#sha256=da69d28dcd527c0e372b3fa7b92fc333b327f8470175f035abc4e351b539189f",
                attrs={
                    "data-gpg-sig": "false",
                    "data-dist-info-metadata": "sha256=true",
                },
            ),
            DistributionPackage(
                filename="qypi-0.1.0-py3-none-any.whl",
                url="https://files.pythonhosted.org/packages/82/fc/9e25534641d7f63be93079bc07fa92bab136ddf5d4181059a1308a346f96/qypi-0.1.0-py3-none-any.whl",
                digests={
                    "sha256": "da69d28dcd527c0e372b3fa7b92fc333b327f8470175f035abc4e351b539189f"
                },
                has_sig=False,
                requires_python=None,
                project="qypi",
                version="0.1.0",
                package_type="wheel",
                is_yanked=False,
                yanked_reason=None,
                metadata_digests={},
                has_metadata=True,
            ),
        ),
    ],
)
def test_from_link(link: Link, distpkg: DistributionPackage) -> None:
    assert DistributionPackage.from_link(link) == distpkg


def test_pep658() -> None:
    pkg = DistributionPackage(
        filename="qypi-0.1.0-py3-none-any.whl",
        url="https://files.pythonhosted.org/packages/82/fc/9e25534641d7f63be93079bc07fa92bab136ddf5d4181059a1308a346f96/qypi-0.1.0-py3-none-any.whl",
        digests={
            "sha256": "da69d28dcd527c0e372b3fa7b92fc333b327f8470175f035abc4e351b539189f"
        },
        has_sig=True,
        requires_python="~= 3.6",
        project="qypi",
        version="0.1.0",
        package_type="wheel",
        is_yanked=False,
        yanked_reason=None,
        metadata_digests={
            "sha256": "ae718719df4708f329d58ca4d5390c1206c4222ef7e62a3aa9844397c63de28b"
        },
        has_metadata=True,
    )
    assert (
        pkg.metadata_url
        == "https://files.pythonhosted.org/packages/82/fc/9e25534641d7f63be93079bc07fa92bab136ddf5d4181059a1308a346f96/qypi-0.1.0-py3-none-any.whl.metadata"
    )


def test_pep658_no_digests() -> None:
    pkg = DistributionPackage(
        filename="qypi-0.1.0-py3-none-any.whl",
        url="https://files.pythonhosted.org/packages/82/fc/9e25534641d7f63be93079bc07fa92bab136ddf5d4181059a1308a346f96/qypi-0.1.0-py3-none-any.whl",
        digests={
            "sha256": "da69d28dcd527c0e372b3fa7b92fc333b327f8470175f035abc4e351b539189f"
        },
        has_sig=True,
        requires_python="~= 3.6",
        project="qypi",
        version="0.1.0",
        package_type="wheel",
        is_yanked=False,
        yanked_reason=None,
        metadata_digests={},
        has_metadata=True,
    )
    assert (
        pkg.metadata_url
        == "https://files.pythonhosted.org/packages/82/fc/9e25534641d7f63be93079bc07fa92bab136ddf5d4181059a1308a346f96/qypi-0.1.0-py3-none-any.whl.metadata"
    )


def test_from_json_data_no_metadata() -> None:
    pkg = DistributionPackage.from_json_data(
        {
            "filename": "argset-0.1.0-py3-none-any.whl",
            "hashes": {
                "sha256": "107a632c7112faceb9fd6e93658dd461154713db250f7ffde5bd473e17cf1db5"
            },
            "requires-python": "~=3.6",
            "url": "https://files.pythonhosted.org/packages/b5/2b/7aa284f345e37f955d86e4cd57b1039b573552b0fc29d1a522ec05c1ee41/argset-0.1.0-py3-none-any.whl",
            "yanked": False,
        }
    )
    assert pkg.has_metadata is None
    assert pkg.metadata_digests is None


@pytest.mark.parametrize(
    "dist_info_metadata,has_metadata,metadata_digests",
    [
        (False, False, None),
        (True, True, {}),
        ({}, True, {}),
        ({"sha256": "abc123"}, True, {"sha256": "abc123"}),
    ],
)
def test_from_json_data_metadata(
    dist_info_metadata: bool | dict[str, str],
    has_metadata: bool,
    metadata_digests: Optional[dict[str, str]],
) -> None:
    pkg = DistributionPackage.from_json_data(
        {
            "filename": "argset-0.1.0-py3-none-any.whl",
            "hashes": {
                "sha256": "107a632c7112faceb9fd6e93658dd461154713db250f7ffde5bd473e17cf1db5"
            },
            "requires-python": "~=3.6",
            "url": "https://files.pythonhosted.org/packages/b5/2b/7aa284f345e37f955d86e4cd57b1039b573552b0fc29d1a522ec05c1ee41/argset-0.1.0-py3-none-any.whl",
            "yanked": False,
            "dist-info-metadata": dist_info_metadata,
        }
    )
    assert pkg.has_metadata == has_metadata
    assert pkg.metadata_digests == metadata_digests
