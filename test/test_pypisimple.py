from   os.path     import dirname, join
import pytest
import responses
from   pypi_simple import DistributionPackage, PyPISimple

@pytest.mark.parametrize('content_type', [
    'text/html',
    'text/html; charset=utf-8',
])
@responses.activate
def test_session(content_type):
    session_dir = join(dirname(__file__), 'data', 'session01')
    with open(join(session_dir, 'simple.html')) as fp:
        responses.add(
            method=responses.GET,
            url='https://test.nil/simple/',
            body=fp.read(),
            content_type=content_type,
        )
    responses.add(
        method=responses.GET,
        url='https://test.nil/simple/',
        body='This URL should only be requested once.',
        status=500,
    )
    with open(join(session_dir, 'in-place.html')) as fp:
        responses.add(
            method=responses.GET,
            url='https://test.nil/simple/in-place/',
            body=fp.read(),
            content_type=content_type,
        )
    responses.add(
        method=responses.GET,
        url='https://test.nil/simple/nonexistent/',
        body='Does not exist',
        status=404,
    )

    simple = PyPISimple('https://test.nil/simple/')
    assert list(simple.get_projects()) == ['in_place', 'foo', 'BAR']
    assert simple.get_project_url('IN.PLACE') == 'https://test.nil/simple/in-place/'

    assert simple.get_project_files('IN.PLACE') == [
        DistributionPackage(
            filename='in_place-0.1.1-py2.py3-none-any.whl',
            project='in_place',
            version='0.1.1',
            package_type='wheel',
            url="https://files.pythonhosted.org/packages/34/81/2baaaa588ee1a6faa6354b7c9bc365f1b3da867707cd136dfedff7c06608/in_place-0.1.1-py2.py3-none-any.whl#sha256=e0732b6bdc2f1bfc4e1b96c1de2fbbd053bb2a9534547474a0485baa339bfa97",
            requires_python=None,
            has_sig=False,
        ),
        DistributionPackage(
            filename='in_place-0.1.1.tar.gz',
            project='in_place',
            version='0.1.1',
            package_type='sdist',
            url="https://files.pythonhosted.org/packages/b9/ba/f1c67fb32c37ba4263326ae4ac6fd00b128025c9289b2fb31a60a0a22f90/in_place-0.1.1.tar.gz#sha256=ffa729fd0b818ac750aa31bafc886f266380e1c8557ba38f70f422d2f6a77e23",
            requires_python=None,
            has_sig=False,
        ),
        DistributionPackage(
            filename='in_place-0.2.0-py2.py3-none-any.whl',
            project='in_place',
            version='0.2.0',
            package_type='wheel',
            url="https://files.pythonhosted.org/packages/9f/46/9f5679f3b2068e10b33c16a628a78b2b36531a9df08671bd0104f11d8461/in_place-0.2.0-py2.py3-none-any.whl#sha256=e1ad42a41dfde02092b411b1634a4be228e28c27553499a81ef04b377b28857c",
            requires_python=None,
            has_sig=False,
        ),
        DistributionPackage(
            filename='in_place-0.2.0.tar.gz',
            project='in_place',
            version='0.2.0',
            package_type='sdist',
            url="https://files.pythonhosted.org/packages/f0/51/c30f1fad2b857f7b5d5ff76ec01f1f80dd0f2ab6b6afcde7b2aed54faa7e/in_place-0.2.0.tar.gz#sha256=ff783dca5d06f85b8d084871abd11a170d732423edb48c53ccb68c55fcbbeb76",
            requires_python=None,
            has_sig=False,
        ),
        DistributionPackage(
            filename='in_place-0.3.0-py2.py3-none-any.whl',
            project='in_place',
            version='0.3.0',
            package_type='wheel',
            url="https://files.pythonhosted.org/packages/6f/84/ced31e646df335f8cd1b7884e3740b8c012314a28504542ef5631cdc1449/in_place-0.3.0-py2.py3-none-any.whl#sha256=af5ce9bd309f85a6bbe4119acbc0a67cda68f0ae616f0a76a947addc62791fda",
            requires_python=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, <4",
            has_sig=False,
        ),
        DistributionPackage(
            filename='in_place-0.3.0.tar.gz',
            project='in_place',
            version='0.3.0',
            package_type='sdist',
            url="https://files.pythonhosted.org/packages/b6/cd/1dc736d5248420b15dd1546c2938aec7e6dab134e698e0768f54f1757af7/in_place-0.3.0.tar.gz#sha256=4758db1457c8addcd5f5b15ef870eab66b238e46e7d784bff99ab1b2126660ea",
            requires_python=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, <4",
            has_sig=False,
        ),
    ]

    assert simple.get_project_files('nonexistent') == []


@responses.activate
def test_project_hint_received():
    """
    Test that the argument to ``get_project_files()`` is used to disambiguate
    filenames
    """
    with open(join(dirname(__file__), 'data', 'aws-adfs-ebsco.html')) as fp:
        responses.add(
            method=responses.GET,
            url='https://test.nil/simple/aws-adfs-ebsco/',
            body=fp.read(),
            content_type='text/html',
        )
    simple = PyPISimple('https://test.nil/simple/')
    assert simple.get_project_files('aws-adfs-ebsco') == [
        DistributionPackage(
            filename='aws-adfs-ebsco-0.3.6-2.tar.gz',
            project='aws-adfs-ebsco',
            version='0.3.6-2',
            package_type='sdist',
            url="https://files.pythonhosted.org/packages/13/b7/a69bdbf294db5ba0973ee45a2b2ce7045030cd922e1c0ca052d102c45b95/aws-adfs-ebsco-0.3.6-2.tar.gz#sha256=6eadd17408e1f26a313bc75afaa3011333bc2915461c446720bafd7608987e1e",
            requires_python=None,
            has_sig=False,
        ),
        DistributionPackage(
            filename='aws-adfs-ebsco-0.3.7-1.tar.gz',
            project='aws-adfs-ebsco',
            version='0.3.7-1',
            package_type='sdist',
            url="https://files.pythonhosted.org/packages/86/8a/46c2a99113cfbb7d6c089b2128ca9e4faaea1f6a1d4e17577fd9a3396bee/aws-adfs-ebsco-0.3.7-1.tar.gz#sha256=7992abc36d0061896a3f06f055e053ffde9f3fcf483340adfa675c65ebfb3f8d",
            requires_python=None,
            has_sig=False,
        ),
    ]

@pytest.mark.parametrize('endpoint', [
    'https://test.nil/simple',
    'https://test.nil/simple/',
])
@pytest.mark.parametrize('project', [
    'some-project',
    'some.project',
    'SOME_PROJECT',
])
def test_get_project_url(endpoint, project):
    assert PyPISimple(endpoint).get_project_url(project) \
        == 'https://test.nil/simple/some-project/'

@responses.activate
def test_redirected_project_page():
    responses.add(
        method=responses.GET,
        url='https://nil.test/simple/project/',
        status=301,
        headers={'Location': 'https://test.nil/simple/project/'},
    )
    responses.add(
        method=responses.GET,
        url='https://test.nil/simple/project/',
        body='<a href="../files/project-0.1.0.tar.gz">project-0.1.0.tar.gz</a>',
        content_type='text/html',
    )
    simple = PyPISimple('https://nil.test/simple/')
    assert simple.get_project_files('project') == [
        DistributionPackage(
            filename='project-0.1.0.tar.gz',
            project='project',
            version='0.1.0',
            package_type='sdist',
            url="https://test.nil/simple/files/project-0.1.0.tar.gz",
            requires_python=None,
            has_sig=False,
        ),
    ]
