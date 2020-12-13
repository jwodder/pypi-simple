from   pathlib     import Path
import pytest
import requests
import responses
from   pypi_simple import DistributionPackage, IndexPage, ProjectPage, \
                            PyPISimple

DATA_DIR = Path(__file__).with_name('data')

@pytest.mark.parametrize('content_type', [
    'text/html',
    'text/html; charset=utf-8',
])
@responses.activate
def test_session(mocker, content_type):
    session_dir = DATA_DIR / 'session01'
    with (session_dir / 'simple.html').open() as fp:
        responses.add(
            method=responses.GET,
            url='https://test.nil/simple/',
            body=fp.read(),
            content_type=content_type,
            headers={"x-pypi-last-serial": "12345"},
        )
    responses.add(
        method=responses.GET,
        url='https://test.nil/simple/',
        body='This URL should only be requested once.',
        status=500,
    )
    with (session_dir / 'in-place.html').open() as fp:
        responses.add(
            method=responses.GET,
            url='https://test.nil/simple/in-place/',
            body=fp.read(),
            content_type=content_type,
            headers={"X-PYPI-LAST-SERIAL": "54321"},
        )
    responses.add(
        method=responses.GET,
        url='https://test.nil/simple/nonexistent/',
        body='Does not exist',
        status=404,
    )
    with PyPISimple('https://test.nil/simple/') as simple:
        spy = mocker.spy(simple.s, 'get')
        assert simple.get_index_page(timeout=3.14) == IndexPage(
            projects=['in_place', 'foo', 'BAR'],
            last_serial='12345',
            repository_version='1.0',
        )
        call, = spy.call_args_list
        assert call[1]["timeout"] == 3.14
        spy.reset_mock()
        assert simple.get_project_url('IN.PLACE') \
            == 'https://test.nil/simple/in-place/'
        assert simple.get_project_page('IN.PLACE', timeout=2.718) == ProjectPage(
            project='IN.PLACE',
            packages=[
                DistributionPackage(
                    filename='in_place-0.1.1-py2.py3-none-any.whl',
                    project='in_place',
                    version='0.1.1',
                    package_type='wheel',
                    url="https://files.pythonhosted.org/packages/34/81/2baaaa588ee1a6faa6354b7c9bc365f1b3da867707cd136dfedff7c06608/in_place-0.1.1-py2.py3-none-any.whl#sha256=e0732b6bdc2f1bfc4e1b96c1de2fbbd053bb2a9534547474a0485baa339bfa97",
                    requires_python=None,
                    has_sig=None,
                    yanked=None,
                ),
                DistributionPackage(
                    filename='in_place-0.1.1.tar.gz',
                    project='in_place',
                    version='0.1.1',
                    package_type='sdist',
                    url="https://files.pythonhosted.org/packages/b9/ba/f1c67fb32c37ba4263326ae4ac6fd00b128025c9289b2fb31a60a0a22f90/in_place-0.1.1.tar.gz#sha256=ffa729fd0b818ac750aa31bafc886f266380e1c8557ba38f70f422d2f6a77e23",
                    requires_python=None,
                    has_sig=None,
                    yanked=None,
                ),
                DistributionPackage(
                    filename='in_place-0.2.0-py2.py3-none-any.whl',
                    project='in_place',
                    version='0.2.0',
                    package_type='wheel',
                    url="https://files.pythonhosted.org/packages/9f/46/9f5679f3b2068e10b33c16a628a78b2b36531a9df08671bd0104f11d8461/in_place-0.2.0-py2.py3-none-any.whl#sha256=e1ad42a41dfde02092b411b1634a4be228e28c27553499a81ef04b377b28857c",
                    requires_python=None,
                    has_sig=None,
                    yanked=None,
                ),
                DistributionPackage(
                    filename='in_place-0.2.0.tar.gz',
                    project='in_place',
                    version='0.2.0',
                    package_type='sdist',
                    url="https://files.pythonhosted.org/packages/f0/51/c30f1fad2b857f7b5d5ff76ec01f1f80dd0f2ab6b6afcde7b2aed54faa7e/in_place-0.2.0.tar.gz#sha256=ff783dca5d06f85b8d084871abd11a170d732423edb48c53ccb68c55fcbbeb76",
                    requires_python=None,
                    has_sig=None,
                    yanked=None,
                ),
                DistributionPackage(
                    filename='in_place-0.3.0-py2.py3-none-any.whl',
                    project='in_place',
                    version='0.3.0',
                    package_type='wheel',
                    url="https://files.pythonhosted.org/packages/6f/84/ced31e646df335f8cd1b7884e3740b8c012314a28504542ef5631cdc1449/in_place-0.3.0-py2.py3-none-any.whl#sha256=af5ce9bd309f85a6bbe4119acbc0a67cda68f0ae616f0a76a947addc62791fda",
                    requires_python=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, <4",
                    has_sig=None,
                    yanked=None,
                ),
                DistributionPackage(
                    filename='in_place-0.3.0.tar.gz',
                    project='in_place',
                    version='0.3.0',
                    package_type='sdist',
                    url="https://files.pythonhosted.org/packages/b6/cd/1dc736d5248420b15dd1546c2938aec7e6dab134e698e0768f54f1757af7/in_place-0.3.0.tar.gz#sha256=4758db1457c8addcd5f5b15ef870eab66b238e46e7d784bff99ab1b2126660ea",
                    requires_python=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, <4",
                    has_sig=None,
                    yanked=None,
                ),
            ],
            last_serial='54321',
            repository_version='1.0',
        )
        call, = spy.call_args_list
        assert call[1]["timeout"] == 2.718
        assert simple.get_project_page('nonexistent') is None

@responses.activate
def test_project_hint_received():
    """
    Test that the argument to ``get_project_page()`` is used to disambiguate
    filenames
    """
    with (DATA_DIR / 'aws-adfs-ebsco.html').open() as fp:
        responses.add(
            method=responses.GET,
            url='https://test.nil/simple/aws-adfs-ebsco/',
            body=fp.read(),
            content_type='text/html',
        )
    with PyPISimple('https://test.nil/simple/') as simple:
        assert simple.get_project_page('aws-adfs-ebsco') == ProjectPage(
            project='aws-adfs-ebsco',
            packages=[
                DistributionPackage(
                    filename='aws-adfs-ebsco-0.3.6-2.tar.gz',
                    project='aws-adfs-ebsco',
                    version='0.3.6-2',
                    package_type='sdist',
                    url="https://files.pythonhosted.org/packages/13/b7/a69bdbf294db5ba0973ee45a2b2ce7045030cd922e1c0ca052d102c45b95/aws-adfs-ebsco-0.3.6-2.tar.gz#sha256=6eadd17408e1f26a313bc75afaa3011333bc2915461c446720bafd7608987e1e",
                    requires_python=None,
                    has_sig=None,
                    yanked=None,
                ),
                DistributionPackage(
                    filename='aws-adfs-ebsco-0.3.7-1.tar.gz',
                    project='aws-adfs-ebsco',
                    version='0.3.7-1',
                    package_type='sdist',
                    url="https://files.pythonhosted.org/packages/86/8a/46c2a99113cfbb7d6c089b2128ca9e4faaea1f6a1d4e17577fd9a3396bee/aws-adfs-ebsco-0.3.7-1.tar.gz#sha256=7992abc36d0061896a3f06f055e053ffde9f3fcf483340adfa675c65ebfb3f8d",
                    requires_python=None,
                    has_sig=None,
                    yanked=None,
                ),
            ],
            last_serial=None,
            repository_version=None,
        )

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
    with PyPISimple(endpoint) as simple:
        assert simple.get_project_url(project) \
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
    with PyPISimple('https://nil.test/simple/') as simple:
        assert simple.get_project_page('project') == ProjectPage(
            project='project',
            packages=[
                DistributionPackage(
                    filename='project-0.1.0.tar.gz',
                    project='project',
                    version='0.1.0',
                    package_type='sdist',
                    url="https://test.nil/simple/files/project-0.1.0.tar.gz",
                    requires_python=None,
                    has_sig=None,
                    yanked=None,
                ),
            ],
            last_serial=None,
            repository_version=None,
        )

@pytest.mark.parametrize('content_type,body_decl', [
    ('text/html; charset=utf-8', b''),
    ('text/html', b'<?xml encoding="utf-8"?>'),
    ('text/html', b'<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>'),
])
@responses.activate
def test_utf8_declarations(content_type, body_decl):
    responses.add(
        method=responses.GET,
        url='https://test.nil/simple/project/',
        body=body_decl + b'<a href="../files/project-0.1.0-p\xC3\xBF42-none-any.whl">project-0.1.0-p\xC3\xBF42-none-any.whl</a>',
        content_type=content_type,
    )
    with PyPISimple('https://test.nil/simple/') as simple:
        assert simple.get_project_page('project') == ProjectPage(
            project='project',
            packages=[
                DistributionPackage(
                    filename='project-0.1.0-p\xFF42-none-any.whl',
                    project='project',
                    version='0.1.0',
                    package_type='wheel',
                    url="https://test.nil/simple/files/project-0.1.0-p\xFF42-none-any.whl",
                    requires_python=None,
                    has_sig=None,
                    yanked=None,
                ),
            ],
            last_serial=None,
            repository_version=None,
        )

@pytest.mark.parametrize('content_type,body_decl', [
    ('text/html; charset=iso-8859-2', b''),
    ('text/html', b'<?xml encoding="iso-8859-2"?>'),
    ('text/html', b'<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-2"/>'),
])
@responses.activate
def test_latin2_declarations(content_type, body_decl):
    # This test is deliberately weird in order to make sure the code is
    # actually paying attention to the encoding declarations and not just
    # assuming UTF-8 because the input happens to be valid UTF-8.
    responses.add(
        method=responses.GET,
        url='https://test.nil/simple/project/',
        body=body_decl + b'<a href="../files/project-0.1.0-p\xC3\xBF42-none-any.whl">project-0.1.0-p\xC3\xBF42-none-any.whl</a>',
        content_type=content_type,
    )
    with PyPISimple('https://test.nil/simple/') as simple:
        assert simple.get_project_page('project') == ProjectPage(
            project='project',
            packages=[
                DistributionPackage(
                    filename='project-0.1.0-p\u0102\u017C42-none-any.whl',
                    project='project',
                    version='0.1.0',
                    package_type='wheel',
                    url="https://test.nil/simple/files/project-0.1.0-p\u0102\u017C42-none-any.whl",
                    requires_python=None,
                    has_sig=None,
                    yanked=None,
                ),
            ],
            last_serial=None,
            repository_version=None,
        )

def test_auth_new_session():
    with PyPISimple('https://test.nil/simple/', auth=('user', 'password')) \
            as simple:
        assert simple.s.auth == ('user', 'password')

def test_custom_session():
    s = requests.Session()
    with PyPISimple('https://test.nil/simple/', session=s) as simple:
        assert simple.s is s
        assert simple.s.auth is None

def test_auth_custom_session():
    with PyPISimple(
        'https://test.nil/simple/',
        auth=('user', 'password'),
        session=requests.Session(),
    ) as simple:
        assert simple.s.auth == ('user', 'password')

def test_auth_override_custom_session():
    s = requests.Session()
    s.auth = ('login', 'secret')
    with PyPISimple(
        'https://test.nil/simple/',
        auth=('user', 'password'),
        session=s,
    ) as simple:
        assert simple.s.auth == ('user', 'password')

@responses.activate
def test_stream_project_names(mocker):
    session_dir = DATA_DIR / 'session01'
    with (session_dir / 'simple.html').open() as fp:
        responses.add(
            method=responses.GET,
            url='https://test.nil/simple/',
            body=fp.read(),
            content_type="text/html",
            headers={"x-pypi-last-serial": "12345"},
            stream=True,
        )
    responses.add(
        method=responses.GET,
        url='https://test.nil/simple/',
        body='This URL should only be requested once.',
        status=500,
    )
    with PyPISimple('https://test.nil/simple/') as simple:
        spy = mocker.spy(simple.s, 'get')
        assert list(simple.stream_project_names(timeout=1.618)) \
            == ['in_place', 'foo', 'BAR']
        call, = spy.call_args_list
        assert call[1]["timeout"] == 1.618
