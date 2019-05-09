import pytest
from   pypi_simple import DistributionPackage

@pytest.mark.parametrize('fragment', ['', '#', '#sha256', '#sha256='])
def test_get_no_digests(fragment):
    pkg = DistributionPackage(
        filename='qypi-0.1.0-py3-none-any.whl',
        project='qypi',
        version='0.1.0',
        package_type='wheel',
        url="https://files.pythonhosted.org/packages/82/fc/9e25534641d7f63be93079bc07fa92bab136ddf5d4181059a1308a346f96/qypi-0.1.0-py3-none-any.whl" + fragment,
        requires_python=None,
        has_sig=False,
        yanked=None,
    )
    assert pkg.get_digests() == {}

def test_get_digests():
    pkg = DistributionPackage(
        filename='qypi-0.1.0-py3-none-any.whl',
        project='qypi',
        version='0.1.0',
        package_type='wheel',
        url="https://files.pythonhosted.org/packages/82/fc/9e25534641d7f63be93079bc07fa92bab136ddf5d4181059a1308a346f96/qypi-0.1.0-py3-none-any.whl#sha256=da69d28dcd527c0e372b3fa7b92fc333b327f8470175f035abc4e351b539189f",
        requires_python=None,
        has_sig=False,
        yanked=None,
    )
    assert pkg.get_digests() == {
        "sha256": "da69d28dcd527c0e372b3fa7b92fc333b327f8470175f035abc4e351b539189f"
    }

def test_get_no_sig_url():
    pkg = DistributionPackage(
        filename='qypi-0.1.0-py3-none-any.whl',
        project='qypi',
        version='0.1.0',
        package_type='wheel',
        url="https://files.pythonhosted.org/packages/82/fc/9e25534641d7f63be93079bc07fa92bab136ddf5d4181059a1308a346f96/qypi-0.1.0-py3-none-any.whl#sha256=da69d28dcd527c0e372b3fa7b92fc333b327f8470175f035abc4e351b539189f",
        requires_python=None,
        has_sig=False,
        yanked=None,
    )
    assert pkg.sig_url is None

def test_get_sig_url():
    pkg = DistributionPackage(
        filename='qypi-0.1.0-py3-none-any.whl',
        project='qypi',
        version='0.1.0',
        package_type='wheel',
        url="https://files.pythonhosted.org/packages/82/fc/9e25534641d7f63be93079bc07fa92bab136ddf5d4181059a1308a346f96/qypi-0.1.0-py3-none-any.whl#sha256=da69d28dcd527c0e372b3fa7b92fc333b327f8470175f035abc4e351b539189f",
        requires_python=None,
        has_sig=True,
        yanked=None,
    )
    assert pkg.sig_url == "https://files.pythonhosted.org/packages/82/fc/9e25534641d7f63be93079bc07fa92bab136ddf5d4181059a1308a346f96/qypi-0.1.0-py3-none-any.whl.asc"
