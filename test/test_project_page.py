import json
from pathlib import Path
import pytest
from pypi_simple import (
    PYPI_SIMPLE_ENDPOINT,
    SUPPORTED_REPOSITORY_VERSION,
    DistributionPackage,
    ProjectPage,
    UnsupportedRepoVersionError,
)

DATA_DIR = Path(__file__).with_name("data")


def test_from_html_empty() -> None:
    assert ProjectPage.from_html("-NIL-", "") == ProjectPage(
        project="-NIL-",
        packages=[],
        repository_version=None,
        last_serial=None,
    )


@pytest.mark.parametrize(
    "project,filename,base_url,encoding,page",
    [
        (
            "qypi",
            "qypi.html",
            PYPI_SIMPLE_ENDPOINT + "qypi/",
            "utf-8",
            ProjectPage(
                project="qypi",
                packages=[
                    DistributionPackage(
                        filename="qypi-0.1.0-py3-none-any.whl",
                        project="qypi",
                        version="0.1.0",
                        package_type="wheel",
                        url="https://files.pythonhosted.org/packages/82/fc/9e25534641d7f63be93079bc07fa92bab136ddf5d4181059a1308a346f96/qypi-0.1.0-py3-none-any.whl",
                        digests={
                            "sha256": "da69d28dcd527c0e372b3fa7b92fc333b327f8470175f035abc4e351b539189f"
                        },
                        requires_python="~=3.4",
                        has_sig=None,
                        is_yanked=False,
                        yanked_reason=None,
                        metadata_digests=None,
                        has_metadata=False,
                    ),
                    DistributionPackage(
                        filename="qypi-0.1.0.tar.gz",
                        project="qypi",
                        version="0.1.0",
                        package_type="sdist",
                        url="https://files.pythonhosted.org/packages/e4/fe/3fdb222a2916b94e9ca12d80c92dbbad1f7068c82fca42872d6c1739fead/qypi-0.1.0.tar.gz",
                        digests={
                            "sha256": "212093de95b4f5f22e19fa18fe57fa33eccd63adb9b325fe1b673bf71912c551"
                        },
                        requires_python="~=3.4",
                        has_sig=None,
                        is_yanked=False,
                        yanked_reason=None,
                        metadata_digests=None,
                        has_metadata=False,
                    ),
                    DistributionPackage(
                        filename="qypi-0.1.0.post1-py3-none-any.whl",
                        project="qypi",
                        version="0.1.0.post1",
                        package_type="wheel",
                        url="https://files.pythonhosted.org/packages/f9/3f/6b184713e79da15cd451f0dab91864633175242f4d321df0cacdd2dc8300/qypi-0.1.0.post1-py3-none-any.whl",
                        digests={
                            "sha256": "5946a4557550479af90278e5418cd2c32a2626936075078a4c7096be52d43078"
                        },
                        requires_python="~=3.4",
                        has_sig=None,
                        is_yanked=False,
                        yanked_reason=None,
                        metadata_digests=None,
                        has_metadata=False,
                    ),
                    DistributionPackage(
                        filename="qypi-0.1.0.post1.tar.gz",
                        project="qypi",
                        version="0.1.0.post1",
                        package_type="sdist",
                        url="https://files.pythonhosted.org/packages/0e/49/3056ee68b44c8eab4d4698b52ae4d18c0db92c80abc312894c02c4722621/qypi-0.1.0.post1.tar.gz",
                        digests={
                            "sha256": "c99eea315455cf9fde722599ab67eeefdff5c184bb3861a7fd82f8a9387c252d"
                        },
                        requires_python="~=3.4",
                        has_sig=None,
                        is_yanked=False,
                        yanked_reason=None,
                        metadata_digests=None,
                        has_metadata=False,
                    ),
                    DistributionPackage(
                        filename="qypi-0.2.0-py3-none-any.whl",
                        project="qypi",
                        version="0.2.0",
                        package_type="wheel",
                        url="https://files.pythonhosted.org/packages/96/b8/9c2d0c3d0d95ccdaa04ebff77f8e85e9ca0888f2844b102d32a81ca3c92e/qypi-0.2.0-py3-none-any.whl",
                        digests={
                            "sha256": "0923d60c5ff6aaf73c4805b5381868ccdf44d1cfe1d1a659d679be821fe38d53"
                        },
                        requires_python="~=3.4",
                        has_sig=None,
                        is_yanked=False,
                        yanked_reason=None,
                        metadata_digests=None,
                        has_metadata=False,
                    ),
                    DistributionPackage(
                        filename="qypi-0.2.0.tar.gz",
                        project="qypi",
                        version="0.2.0",
                        package_type="sdist",
                        url="https://files.pythonhosted.org/packages/f6/6a/1d37c72684c19f28060bd7ed1bfe3bfb8c6b9b1132b0ea67f98c036930da/qypi-0.2.0.tar.gz",
                        digests={
                            "sha256": "cf24ea8841d0f10a822fd5cf3809c1324e5b1eab34e148b841dae6ad54919c85"
                        },
                        requires_python="~=3.4",
                        has_sig=None,
                        is_yanked=False,
                        yanked_reason=None,
                        metadata_digests=None,
                        has_metadata=False,
                    ),
                    DistributionPackage(
                        filename="qypi-0.3.0-py3-none-any.whl",
                        project="qypi",
                        version="0.3.0",
                        package_type="wheel",
                        url="https://files.pythonhosted.org/packages/79/b4/dbdcc76c55d1714f2d51f1da25c2a8a59cd1e35357bcafefb7ef6efd8c78/qypi-0.3.0-py3-none-any.whl",
                        digests={
                            "sha256": "4dddbfa57d6b0c23a0cc20aa17aa8b17c4b41bcbd57c8d273dad84601e85e2dd"
                        },
                        requires_python="~=3.4",
                        has_sig=None,
                        is_yanked=False,
                        yanked_reason=None,
                        metadata_digests=None,
                        has_metadata=False,
                    ),
                    DistributionPackage(
                        filename="qypi-0.3.0.tar.gz",
                        project="qypi",
                        version="0.3.0",
                        package_type="sdist",
                        url="https://files.pythonhosted.org/packages/46/08/08f54b999c68fb1973824d4ac290a872136e978c6747dca647fc8116c59f/qypi-0.3.0.tar.gz",
                        digests={
                            "sha256": "d23f45234a2f7431bd331b9fd4dedc0ff8de1361e171f4f47bb83a15b5726ba1"
                        },
                        requires_python="~=3.4",
                        has_sig=None,
                        is_yanked=False,
                        yanked_reason=None,
                        metadata_digests=None,
                        has_metadata=False,
                    ),
                    DistributionPackage(
                        filename="qypi-0.4.0-py3-none-any.whl",
                        project="qypi",
                        version="0.4.0",
                        package_type="wheel",
                        url="https://files.pythonhosted.org/packages/b9/29/82545bfa0b65f8ace22e154f0dd26c3543101523ea86df668995abafcf85/qypi-0.4.0-py3-none-any.whl",
                        digests={
                            "sha256": "f264f87c34b722afdfde2349999697418e404183c80e5180032b3d61202e9a4d"
                        },
                        requires_python="~=3.4",
                        has_sig=None,
                        is_yanked=False,
                        yanked_reason=None,
                        metadata_digests=None,
                        has_metadata=False,
                    ),
                    DistributionPackage(
                        filename="qypi-0.4.0.tar.gz",
                        project="qypi",
                        version="0.4.0",
                        package_type="sdist",
                        url="https://files.pythonhosted.org/packages/4a/77/c4cd613177fcc894408ba731abc9d3392dcdd4cc9d6be8f1899c942686dd/qypi-0.4.0.tar.gz",
                        digests={
                            "sha256": "884d59dd776e091b610e967729a57dd29fe095125210ef29ec4f874245baf7b6"
                        },
                        requires_python="~=3.4",
                        has_sig=None,
                        is_yanked=False,
                        yanked_reason=None,
                        metadata_digests=None,
                        has_metadata=False,
                    ),
                    DistributionPackage(
                        filename="qypi-0.4.1-py3-none-any.whl",
                        project="qypi",
                        version="0.4.1",
                        package_type="wheel",
                        url="https://files.pythonhosted.org/packages/b3/43/ac36d6a00a86ba7dc9c61f3dd448c233aae2c014c6cae111908ca5644112/qypi-0.4.1-py3-none-any.whl",
                        digests={
                            "sha256": "488a65d6bd8c10f211e098d2d6e4a66df003be12f028b8f6f858ac2863579eb1"
                        },
                        requires_python="~=3.4",
                        has_sig=None,
                        is_yanked=False,
                        yanked_reason=None,
                        metadata_digests=None,
                        has_metadata=False,
                    ),
                    DistributionPackage(
                        filename="qypi-0.4.1.tar.gz",
                        project="qypi",
                        version="0.4.1",
                        package_type="sdist",
                        url="https://files.pythonhosted.org/packages/70/7f/8da79c0732787236a9a3a7787f2abfaf996f96f6ebccfdb533646f70640e/qypi-0.4.1.tar.gz",
                        digests={
                            "sha256": "5f69adbf25e8369d25c31e41912ed0e6be429beb62faf4fc424aa667c561f657"
                        },
                        requires_python="~=3.4",
                        has_sig=None,
                        is_yanked=False,
                        yanked_reason=None,
                        metadata_digests=None,
                        has_metadata=False,
                    ),
                ],
                repository_version=None,
                last_serial=None,
            ),
        ),
        (
            "qypi",
            "qypi_base.html",
            PYPI_SIMPLE_ENDPOINT + "qypi/",
            "utf-8",
            ProjectPage(
                project="qypi",
                packages=[
                    DistributionPackage(
                        filename="qypi-0.1.0-py3-none-any.whl",
                        project="qypi",
                        version="0.1.0",
                        package_type="wheel",
                        url="https://files.pythonhosted.org/packages/82/fc/9e25534641d7f63be93079bc07fa92bab136ddf5d4181059a1308a346f96/qypi-0.1.0-py3-none-any.whl",
                        digests={
                            "sha256": "da69d28dcd527c0e372b3fa7b92fc333b327f8470175f035abc4e351b539189f"
                        },
                        requires_python="~=3.4",
                        has_sig=None,
                        is_yanked=False,
                        yanked_reason=None,
                        metadata_digests=None,
                        has_metadata=False,
                    ),
                    DistributionPackage(
                        filename="qypi-0.1.0.tar.gz",
                        project="qypi",
                        version="0.1.0",
                        package_type="sdist",
                        url="https://files.pythonhosted.org/packages/e4/fe/3fdb222a2916b94e9ca12d80c92dbbad1f7068c82fca42872d6c1739fead/qypi-0.1.0.tar.gz",
                        digests={
                            "sha256": "212093de95b4f5f22e19fa18fe57fa33eccd63adb9b325fe1b673bf71912c551"
                        },
                        requires_python="~=3.4",
                        has_sig=None,
                        is_yanked=False,
                        yanked_reason=None,
                        metadata_digests=None,
                        has_metadata=False,
                    ),
                    DistributionPackage(
                        filename="qypi-0.1.0.post1-py3-none-any.whl",
                        project="qypi",
                        version="0.1.0.post1",
                        package_type="wheel",
                        url="https://files.pythonhosted.org/packages/f9/3f/6b184713e79da15cd451f0dab91864633175242f4d321df0cacdd2dc8300/qypi-0.1.0.post1-py3-none-any.whl",
                        digests={
                            "sha256": "5946a4557550479af90278e5418cd2c32a2626936075078a4c7096be52d43078"
                        },
                        requires_python="~=3.4",
                        has_sig=None,
                        is_yanked=False,
                        yanked_reason=None,
                        metadata_digests=None,
                        has_metadata=False,
                    ),
                    DistributionPackage(
                        filename="qypi-0.1.0.post1.tar.gz",
                        project="qypi",
                        version="0.1.0.post1",
                        package_type="sdist",
                        url="https://files.pythonhosted.org/packages/0e/49/3056ee68b44c8eab4d4698b52ae4d18c0db92c80abc312894c02c4722621/qypi-0.1.0.post1.tar.gz",
                        digests={
                            "sha256": "c99eea315455cf9fde722599ab67eeefdff5c184bb3861a7fd82f8a9387c252d"
                        },
                        requires_python="~=3.4",
                        has_sig=None,
                        is_yanked=False,
                        yanked_reason=None,
                        metadata_digests=None,
                        has_metadata=False,
                    ),
                ],
                repository_version=None,
                last_serial=None,
            ),
        ),
        (
            "qypi",
            "qypi_mixed.html",
            PYPI_SIMPLE_ENDPOINT + "qypi/",
            "utf-8",
            ProjectPage(
                project="qypi",
                packages=[
                    DistributionPackage(
                        filename="qypi-0.1.0-py3-none-any.whl",
                        project="qypi",
                        version="0.1.0",
                        package_type="wheel",
                        url="https://files.pythonhosted.org/packages/82/fc/9e25534641d7f63be93079bc07fa92bab136ddf5d4181059a1308a346f96/qypi-0.1.0-py3-none-any.whl",
                        digests={
                            "sha256": "da69d28dcd527c0e372b3fa7b92fc333b327f8470175f035abc4e351b539189f"
                        },
                        requires_python=None,
                        has_sig=None,
                        is_yanked=True,
                        yanked_reason="Metadata was smelly",
                        metadata_digests=None,
                        has_metadata=False,
                    ),
                    DistributionPackage(
                        filename="qypi-0.1.0.tar.gz",
                        project="qypi",
                        version="0.1.0",
                        package_type="sdist",
                        url="https://files.pythonhosted.org/packages/e4/fe/3fdb222a2916b94e9ca12d80c92dbbad1f7068c82fca42872d6c1739fead/qypi-0.1.0.tar.gz",
                        digests={
                            "sha256": "212093de95b4f5f22e19fa18fe57fa33eccd63adb9b325fe1b673bf71912c551"
                        },
                        requires_python="~=3.4",
                        has_sig=None,
                        is_yanked=True,
                        yanked_reason="",
                        metadata_digests=None,
                        has_metadata=False,
                    ),
                    DistributionPackage(
                        filename="qypi-0.1.0.post1-py3-none-any.whl",
                        project="qypi",
                        version="0.1.0.post1",
                        package_type="wheel",
                        url="https://files.pythonhosted.org/packages/f9/3f/6b184713e79da15cd451f0dab91864633175242f4d321df0cacdd2dc8300/qypi-0.1.0.post1-py3-none-any.whl",
                        digests={
                            "sha256": "5946a4557550479af90278e5418cd2c32a2626936075078a4c7096be52d43078"
                        },
                        requires_python=None,
                        has_sig=True,
                        is_yanked=True,
                        yanked_reason="",
                        metadata_digests=None,
                        has_metadata=False,
                    ),
                    DistributionPackage(
                        filename="qypi-0.1.0.post1.tar.gz",
                        project="qypi",
                        version="0.1.0.post1",
                        package_type="sdist",
                        url="https://files.pythonhosted.org/packages/0e/49/3056ee68b44c8eab4d4698b52ae4d18c0db92c80abc312894c02c4722621/qypi-0.1.0.post1.tar.gz",
                        digests={
                            "sha256": "c99eea315455cf9fde722599ab67eeefdff5c184bb3861a7fd82f8a9387c252d"
                        },
                        requires_python="~=3.4",
                        has_sig=True,
                        is_yanked=False,
                        yanked_reason=None,
                        metadata_digests=None,
                        has_metadata=False,
                    ),
                    DistributionPackage(
                        filename="qypi-0.2.0-py3-none-any.whl",
                        project="qypi",
                        version="0.2.0",
                        package_type="wheel",
                        url="https://files.pythonhosted.org/packages/96/b8/9c2d0c3d0d95ccdaa04ebff77f8e85e9ca0888f2844b102d32a81ca3c92e/qypi-0.2.0-py3-none-any.whl",
                        digests={
                            "sha256": "0923d60c5ff6aaf73c4805b5381868ccdf44d1cfe1d1a659d679be821fe38d53"
                        },
                        requires_python=None,
                        has_sig=False,
                        is_yanked=False,
                        yanked_reason=None,
                        metadata_digests=None,
                        has_metadata=False,
                    ),
                ],
                repository_version=None,
                last_serial=None,
            ),
        ),
        (
            "qypi",
            "qypi_repo_version.html",
            PYPI_SIMPLE_ENDPOINT + "qypi/",
            "utf-8",
            ProjectPage(
                project="qypi",
                packages=[
                    DistributionPackage(
                        filename="qypi-0.1.0-py3-none-any.whl",
                        project="qypi",
                        version="0.1.0",
                        package_type="wheel",
                        url="https://files.pythonhosted.org/packages/82/fc/9e25534641d7f63be93079bc07fa92bab136ddf5d4181059a1308a346f96/qypi-0.1.0-py3-none-any.whl",
                        digests={
                            "sha256": "da69d28dcd527c0e372b3fa7b92fc333b327f8470175f035abc4e351b539189f"
                        },
                        requires_python="~=3.4",
                        has_sig=None,
                        is_yanked=False,
                        yanked_reason=None,
                        metadata_digests=None,
                        has_metadata=False,
                    ),
                    DistributionPackage(
                        filename="qypi-0.1.0.tar.gz",
                        project="qypi",
                        version="0.1.0",
                        package_type="sdist",
                        url="https://files.pythonhosted.org/packages/e4/fe/3fdb222a2916b94e9ca12d80c92dbbad1f7068c82fca42872d6c1739fead/qypi-0.1.0.tar.gz",
                        digests={
                            "sha256": "212093de95b4f5f22e19fa18fe57fa33eccd63adb9b325fe1b673bf71912c551"
                        },
                        requires_python="~=3.4",
                        has_sig=None,
                        is_yanked=False,
                        yanked_reason=None,
                        metadata_digests=None,
                        has_metadata=False,
                    ),
                ],
                repository_version="1.0",
                last_serial=None,
            ),
        ),
        (
            "devpi",
            "devpi_devpi.html",
            "https://m.devpi.net/fschulze/dev/+simple/devpi",
            "utf-8",
            ProjectPage(
                project="devpi",
                packages=[
                    DistributionPackage(
                        filename="devpi-2.2.0.tar.gz",
                        project="devpi",
                        version="2.2.0",
                        package_type="sdist",
                        url="https://m.devpi.net/root/pypi/+f/159/5e5f095022ce7/devpi-2.2.0.tar.gz",
                        digests={
                            "sha256": "1595e5f095022ce7b569326ddceef5d638d936cfb79578d7fc472d46c556cd30"
                        },
                        requires_python=None,
                        has_sig=None,
                        is_yanked=False,
                        yanked_reason=None,
                        metadata_digests=None,
                        has_metadata=False,
                    ),
                    DistributionPackage(
                        filename="devpi-2.1.0.tar.gz",
                        project="devpi",
                        version="2.1.0",
                        package_type="sdist",
                        url="https://m.devpi.net/root/pypi/+f/453/c95c8472d6645/devpi-2.1.0.tar.gz",
                        digests={
                            "sha256": "453c95c8472d66456fd4b3a1526f7f9523f77095111068ef0d60e0dd97e5da27"
                        },
                        requires_python=None,
                        has_sig=None,
                        is_yanked=False,
                        yanked_reason=None,
                        metadata_digests=None,
                        has_metadata=False,
                    ),
                    DistributionPackage(
                        filename="devpi-2.0.3.tar.gz",
                        project="devpi",
                        version="2.0.3",
                        package_type="sdist",
                        url="https://m.devpi.net/fschulze/dev/+f/197/3b59b5a67362a/devpi-2.0.3.tar.gz",
                        digests={
                            "sha256": "1973b59b5a67362a44fbbcee6a5f078f221c5d6d5545215045b5ceb1fdb477c6"
                        },
                        requires_python=None,
                        has_sig=None,
                        is_yanked=False,
                        yanked_reason=None,
                        metadata_digests=None,
                        has_metadata=False,
                    ),
                    DistributionPackage(
                        filename="devpi-2.0.2.tar.gz",
                        project="devpi",
                        version="2.0.2",
                        package_type="sdist",
                        url="https://m.devpi.net/root/pypi/+f/ed6/87407ee52c7da/devpi-2.0.2.tar.gz",
                        digests={
                            "sha256": "ed687407ee52c7dacaaf5d51634a69464cf26c568acee87f6ce595ac3de261e5"
                        },
                        requires_python=None,
                        has_sig=None,
                        is_yanked=False,
                        yanked_reason=None,
                        metadata_digests=None,
                        has_metadata=False,
                    ),
                    DistributionPackage(
                        filename="devpi-2.0.1.tar.gz",
                        project="devpi",
                        version="2.0.1",
                        package_type="sdist",
                        url="https://m.devpi.net/root/pypi/+f/bc1/475505afa93aa/devpi-2.0.1.tar.gz",
                        digests={
                            "sha256": "bc1475505afa93aa41a8fe10249406c4e8804dce4d014ca802807505e3f7594a"
                        },
                        requires_python=None,
                        has_sig=None,
                        is_yanked=False,
                        yanked_reason=None,
                        metadata_digests=None,
                        has_metadata=False,
                    ),
                ],
                repository_version=None,
                last_serial=None,
            ),
        ),
    ],
)
def test_from_html(
    project: str, filename: str, base_url: str, encoding: str, page: ProjectPage
) -> None:
    html = (DATA_DIR / filename).read_bytes()
    assert ProjectPage.from_html(project, html, base_url, encoding) == page


def test_from_html_unsupported_version() -> None:
    with pytest.raises(UnsupportedRepoVersionError) as excinfo:
        ProjectPage.from_html(
            "qypi",
            """
                <!DOCTYPE html>
                <html>
                  <head>
                    <title>Links for qypi</title>
                    <meta name="pypi:repository-version" content="42.0"/>
                  </head>
                  <body>
                    <h1>Links for qypi</h1>
                    <a href="https://files.pythonhosted.org/packages/82/fc/9e25534641d7f63be93079bc07fa92bab136ddf5d4181059a1308a346f96/qypi-0.1.0-py3-none-any.whl#sha256=da69d28dcd527c0e372b3fa7b92fc333b327f8470175f035abc4e351b539189f" data-requires-python="~=3.4">qypi-0.1.0-py3-none-any.whl</a><br/>
                    <a href="https://files.pythonhosted.org/packages/e4/fe/3fdb222a2916b94e9ca12d80c92dbbad1f7068c82fca42872d6c1739fead/qypi-0.1.0.tar.gz#sha256=212093de95b4f5f22e19fa18fe57fa33eccd63adb9b325fe1b673bf71912c551" data-requires-python="~=3.4">qypi-0.1.0.tar.gz</a><br/>
                    </body>
                </html>
                <!--SERIAL 2875636-->
            """,
        )
    assert excinfo.value.declared_version == "42.0"
    assert excinfo.value.supported_version == SUPPORTED_REPOSITORY_VERSION
    assert str(excinfo.value) == (
        "Repository's version (42.0) has greater major component than"
        f" supported version ({SUPPORTED_REPOSITORY_VERSION})"
    )


def test_from_json_data_empty() -> None:
    assert ProjectPage.from_json_data(
        {"files": [], "name": "-NIL-", "meta": {"api-version": "1.0"}}
    ) == ProjectPage(
        project="-NIL-",
        packages=[],
        repository_version="1.0",
        last_serial=None,
    )


@pytest.mark.parametrize(
    "filename,page",
    [
        (
            "argset.json",
            ProjectPage(
                project="argset",
                packages=[
                    DistributionPackage(
                        filename="argset-0.1.0-py3-none-any.whl",
                        project="argset",
                        version="0.1.0",
                        package_type="wheel",
                        url="https://files.pythonhosted.org/packages/b5/2b/7aa284f345e37f955d86e4cd57b1039b573552b0fc29d1a522ec05c1ee41/argset-0.1.0-py3-none-any.whl",
                        requires_python="~=3.6",
                        has_sig=None,
                        is_yanked=False,
                        yanked_reason=None,
                        metadata_digests=None,
                        has_metadata=None,
                        digests={
                            "sha256": "107a632c7112faceb9fd6e93658dd461154713db250f7ffde5bd473e17cf1db5"
                        },
                    ),
                    DistributionPackage(
                        filename="argset-0.1.0.tar.gz",
                        project="argset",
                        version="0.1.0",
                        package_type="sdist",
                        url="https://files.pythonhosted.org/packages/d0/ee/1c25e68d029e8daaf3228dababbf3261fa5d9569f6f705867b2ad4df9b6d/argset-0.1.0.tar.gz",
                        requires_python="~=3.6",
                        has_sig=None,
                        is_yanked=False,
                        yanked_reason=None,
                        metadata_digests=None,
                        has_metadata=None,
                        digests={
                            "sha256": "8a41ee4789d37517c259984c11f2aa3639a90dc8fa446ff905ecc5fe6623c12d"
                        },
                    ),
                ],
                repository_version="1.0",
                last_serial="10562871",
            ),
        ),
        (
            "yanked.json",
            ProjectPage(
                project="yanked",
                packages=[
                    DistributionPackage(
                        filename="yanked-0.0.0-py3-none-any.whl",
                        project="yanked",
                        version="0.0.0",
                        package_type="wheel",
                        url="https://files.pythonhosted.org/packages/9b/af/67c4c6b7f98f2789e4073a0b589f71ad865b3bb8d3e508c51d5f70962fb1/yanked-0.0.0-py3-none-any.whl",
                        requires_python="",
                        has_sig=None,
                        is_yanked=True,
                        yanked_reason=None,
                        metadata_digests=None,
                        has_metadata=None,
                        digests={
                            "sha256": "81aaff3b2a51d570771c32656909950387c7380d321b0305aaad1cd692645932"
                        },
                    ),
                    DistributionPackage(
                        filename="yanked-0.0.0.tar.gz",
                        project="yanked",
                        version="0.0.0",
                        package_type="sdist",
                        url="https://files.pythonhosted.org/packages/2c/9b/23d7985793a487f53fdfbc78e6180cb74b293d200da94895a8a932a4ccc6/yanked-0.0.0.tar.gz",
                        requires_python="",
                        has_sig=None,
                        is_yanked=True,
                        yanked_reason="not good",
                        metadata_digests=None,
                        has_metadata=None,
                        digests={
                            "sha256": "ca14bde2c9c14a5fe7ad9ab9078fdcd8fe09b6de4ca341cc9c286159a8acba41"
                        },
                    ),
                ],
                repository_version="1.0",
                last_serial=None,
            ),
        ),
    ],
)
def test_from_json_data(filename: str, page: ProjectPage) -> None:
    with (DATA_DIR / filename).open() as fp:
        data = json.load(fp)
    assert ProjectPage.from_json_data(data) == page


def test_from_json_data_relative_urls() -> None:
    with (DATA_DIR / "argset-relative.json").open() as fp:
        data = json.load(fp)
    assert ProjectPage.from_json_data(
        data, "https://test.nil/simple/argset/"
    ) == ProjectPage(
        project="argset",
        packages=[
            DistributionPackage(
                filename="argset-0.1.0-py3-none-any.whl",
                project="argset",
                version="0.1.0",
                package_type="wheel",
                url="https://test.nil/simple/argset/packages/argset-0.1.0-py3-none-any.whl",
                requires_python="~=3.6",
                has_sig=None,
                is_yanked=False,
                yanked_reason=None,
                metadata_digests=None,
                has_metadata=None,
                digests={
                    "sha256": "107a632c7112faceb9fd6e93658dd461154713db250f7ffde5bd473e17cf1db5"
                },
            ),
            DistributionPackage(
                filename="argset-0.1.0.tar.gz",
                project="argset",
                version="0.1.0",
                package_type="sdist",
                url="https://test.nil/simple/argset/packages/argset-0.1.0.tar.gz",
                requires_python="~=3.6",
                has_sig=None,
                is_yanked=False,
                yanked_reason=None,
                metadata_digests=None,
                has_metadata=None,
                digests={
                    "sha256": "8a41ee4789d37517c259984c11f2aa3639a90dc8fa446ff905ecc5fe6623c12d"
                },
            ),
        ],
        repository_version="1.0",
        last_serial="10562871",
    )


def test_from_json_data_unsupported_version() -> None:
    with pytest.raises(UnsupportedRepoVersionError) as excinfo:
        ProjectPage.from_json_data(
            {
                "files": [],
                "meta": {"api-version": "42.0"},
                "name": "futuristic",
            },
        )
    assert excinfo.value.declared_version == "42.0"
    assert excinfo.value.supported_version == SUPPORTED_REPOSITORY_VERSION
    assert str(excinfo.value) == (
        "Repository's version (42.0) has greater major component than"
        f" supported version ({SUPPORTED_REPOSITORY_VERSION})"
    )
