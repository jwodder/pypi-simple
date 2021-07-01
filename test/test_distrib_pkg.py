import pytest
from pypi_simple import DistributionPackage, Link


@pytest.mark.parametrize("fragment", ["", "#", "#sha256", "#sha256="])
def test_get_no_digests(fragment):
    pkg = DistributionPackage(
        filename="qypi-0.1.0-py3-none-any.whl",
        project="qypi",
        version="0.1.0",
        package_type="wheel",
        url="https://files.pythonhosted.org/packages/82/fc/9e25534641d7f63be93079bc07fa92bab136ddf5d4181059a1308a346f96/qypi-0.1.0-py3-none-any.whl"
        + fragment,
        requires_python=None,
        has_sig=False,
        yanked=None,
        metadata_digests=None,
    )
    assert pkg.get_digests() == {}


def test_get_digests():
    pkg = DistributionPackage(
        filename="qypi-0.1.0-py3-none-any.whl",
        project="qypi",
        version="0.1.0",
        package_type="wheel",
        url="https://files.pythonhosted.org/packages/82/fc/9e25534641d7f63be93079bc07fa92bab136ddf5d4181059a1308a346f96/qypi-0.1.0-py3-none-any.whl#sha256=da69d28dcd527c0e372b3fa7b92fc333b327f8470175f035abc4e351b539189f",
        requires_python=None,
        has_sig=False,
        yanked=None,
        metadata_digests=None,
    )
    assert pkg.get_digests() == {
        "sha256": "da69d28dcd527c0e372b3fa7b92fc333b327f8470175f035abc4e351b539189f"
    }


@pytest.mark.parametrize("has_sig", [True, False])
def test_get_sig_url(has_sig):
    pkg = DistributionPackage(
        filename="qypi-0.1.0-py3-none-any.whl",
        project="qypi",
        version="0.1.0",
        package_type="wheel",
        url="https://files.pythonhosted.org/packages/82/fc/9e25534641d7f63be93079bc07fa92bab136ddf5d4181059a1308a346f96/qypi-0.1.0-py3-none-any.whl#sha256=da69d28dcd527c0e372b3fa7b92fc333b327f8470175f035abc4e351b539189f",
        requires_python=None,
        has_sig=has_sig,
        yanked=None,
        metadata_digests=None,
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
                url="https://files.pythonhosted.org/packages/82/fc/9e25534641d7f63be93079bc07fa92bab136ddf5d4181059a1308a346f96/qypi-0.1.0-py3-none-any.whl#sha256=da69d28dcd527c0e372b3fa7b92fc333b327f8470175f035abc4e351b539189f",
                has_sig=None,
                requires_python=None,
                project="qypi",
                version="0.1.0",
                package_type="wheel",
                yanked=None,
                metadata_digests=None,
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
                url="https://files.pythonhosted.org/packages/82/fc/9e25534641d7f63be93079bc07fa92bab136ddf5d4181059a1308a346f96/qypi-0.1.0-py3-none-any.whl#sha256=da69d28dcd527c0e372b3fa7b92fc333b327f8470175f035abc4e351b539189f",
                has_sig=True,
                requires_python="~= 3.6",
                project="qypi",
                version="0.1.0",
                package_type="wheel",
                yanked="Oopsy.",
                metadata_digests={
                    "sha256": "ae718719df4708f329d58ca4d5390c1206c4222ef7e62a3aa9844397c63de28b"
                },
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
                url="https://files.pythonhosted.org/packages/82/fc/9e25534641d7f63be93079bc07fa92bab136ddf5d4181059a1308a346f96/qypi-0.1.0-py3-none-any.whl#sha256=da69d28dcd527c0e372b3fa7b92fc333b327f8470175f035abc4e351b539189f",
                has_sig=False,
                requires_python=None,
                project="qypi",
                version="0.1.0",
                package_type="wheel",
                yanked=None,
                metadata_digests={},
            ),
        ),
    ],
)
def test_from_link(link, distpkg):
    assert DistributionPackage.from_link(link) == distpkg


def test_pep658():
    pkg = DistributionPackage(
        filename="qypi-0.1.0-py3-none-any.whl",
        url="https://files.pythonhosted.org/packages/82/fc/9e25534641d7f63be93079bc07fa92bab136ddf5d4181059a1308a346f96/qypi-0.1.0-py3-none-any.whl#sha256=da69d28dcd527c0e372b3fa7b92fc333b327f8470175f035abc4e351b539189f",
        has_sig=True,
        requires_python="~= 3.6",
        project="qypi",
        version="0.1.0",
        package_type="wheel",
        yanked=None,
        metadata_digests={
            "sha256": "ae718719df4708f329d58ca4d5390c1206c4222ef7e62a3aa9844397c63de28b"
        },
    )
    assert pkg.has_metadata is True
    assert (
        pkg.metadata_url
        == "https://files.pythonhosted.org/packages/82/fc/9e25534641d7f63be93079bc07fa92bab136ddf5d4181059a1308a346f96/qypi-0.1.0-py3-none-any.whl.metadata"
    )


def test_pep658_no_digests():
    pkg = DistributionPackage(
        filename="qypi-0.1.0-py3-none-any.whl",
        url="https://files.pythonhosted.org/packages/82/fc/9e25534641d7f63be93079bc07fa92bab136ddf5d4181059a1308a346f96/qypi-0.1.0-py3-none-any.whl#sha256=da69d28dcd527c0e372b3fa7b92fc333b327f8470175f035abc4e351b539189f",
        has_sig=True,
        requires_python="~= 3.6",
        project="qypi",
        version="0.1.0",
        package_type="wheel",
        yanked=None,
        metadata_digests={},
    )
    assert pkg.has_metadata is True
    assert (
        pkg.metadata_url
        == "https://files.pythonhosted.org/packages/82/fc/9e25534641d7f63be93079bc07fa92bab136ddf5d4181059a1308a346f96/qypi-0.1.0-py3-none-any.whl.metadata"
    )


def test_pep658_no_metadata():
    pkg = DistributionPackage(
        filename="qypi-0.1.0-py3-none-any.whl",
        url="https://files.pythonhosted.org/packages/82/fc/9e25534641d7f63be93079bc07fa92bab136ddf5d4181059a1308a346f96/qypi-0.1.0-py3-none-any.whl#sha256=da69d28dcd527c0e372b3fa7b92fc333b327f8470175f035abc4e351b539189f",
        has_sig=True,
        requires_python="~= 3.6",
        project="qypi",
        version="0.1.0",
        package_type="wheel",
        yanked=None,
        metadata_digests=None,
    )
    assert pkg.has_metadata is False
    assert pkg.metadata_url is None
