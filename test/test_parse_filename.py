import pytest
from   pypi_simple import parse_filename

@pytest.mark.parametrize('filename,expected', [
    # dumb:
    ("4ch-1.0.0.linux-x86_64.tar.gz", ('4ch', '1.0.0', 'dumb')),
    (
        "AccelBrainBeat-1.0.0.win-amd64.zip",
        ("AccelBrainBeat", "1.0.0", 'dumb'),
    ),
    (
        "Appengine-Fixture-Loader-0.1.8.linux-x86_64.tar.gz",
        ("Appengine-Fixture-Loader", "0.1.8", 'dumb'),
    ),
    (
        "Appium-Python-Client-0.3.macosx-10.9-intel.tar.gz",
        ("Appium-Python-Client", "0.3", 'dumb'),
    ),
    (
        'linesep-1.0.0.post1.linux-x86_64.tar.gz',
        ('linesep', '1.0.0.post1', 'dumb'),
    ),
    (
        'pypi-simple-0.1.0.dev1.linux-x86_64.tar.gz',
        ('pypi-simple', '0.1.0.dev1', 'dumb'),
    ),

    # egg:
    ("4Suite_XML-1.0rc2-py2.5-win32-2.5.egg", ('4Suite_XML', '1.0rc2', 'egg')),
    ("4Suite_XML-1.0.1-py2.5-win32.egg", ('4Suite_XML', '1.0.1', 'egg')),
    ('btk-0.3.0-py2.7_macosx-10.7-intel.egg', ('btk', '0.3.0', 'egg')),
    ('pypi_simple-0.1.0.dev1-py3.5.egg', ('pypi_simple', '0.1.0.dev1', 'egg')),
    ('setuptools_scm-3.1.0-py2.7.egg', ('setuptools_scm', '3.1.0', 'egg')),

    # msi:
    ('ntracer-0.6.2.pentium4-py2.7.msi', ('ntracer', '0.6.2', 'msi')),
    ('pyFAI-0.13.1.win-amd64-py2.7-1.msi', ('pyFAI', '0.13.1', 'msi')),
    ('pyftpsync-1.1.0-win32.msi', ('pyftpsync', '1.1.0', 'msi')),
    ('pyOpenSSL-0.13.winxp32-py3.2.msi', ('pyOpenSSL', '0.13', 'msi')),
    ('pytango-9.2.0.Win32-py2.7.msi', ('pytango', '9.2.0', 'msi')),
    ("winappdbg-1.3.win32-py2.4.msi", ('winappdbg', '1.3', 'msi')),
    ("winappdbg-1.3.win-amd64-py2.4.msi", ('winappdbg', '1.3', 'msi')),
    ("winappdbg-1.4.win32.msi", ('winappdbg', '1.4', 'msi')),
    ("winappdbg-1.4.win-amd64.msi", ('winappdbg', '1.4', 'msi')),

    # sdist:
    ("1-1.0.0.zip", ('1', '1.0.0', 'sdist')),
    ("3-1-1.0.0.zip", ('3-1', '1.0.0', 'sdist')),
    ("3color-Press-0.2.0.tar.bz2", ('3color-Press', '0.2.0', 'sdist')),
    ("3to2_py3k-0.1b1.tar.gz", ('3to2_py3k', '0.1b1', 'sdist')),
    ('amqplib-1.0.0.tgz', ('amqplib', '1.0.0', 'sdist')),
    (
        "application_repository-0.1.post2.dev31171108.tar.gz",
        ("application_repository", "0.1.post2.dev31171108", 'sdist'),
    ),
    ('pip-18.0.tar.gz', ('pip', '18.0', 'sdist')),
    ('pypi-simple-0.1.0.dev1.tar.gz', ('pypi-simple', '0.1.0.dev1', 'sdist')),
    ('pytz-2008a.tar.bz2', ('pytz', '2008a', 'sdist')),
    ('setuptools-40.2.0.zip', ('setuptools', '40.2.0', 'sdist')),

    # wheel:
    (
        "carbonara_archinfo-7.7.9.14.post1-py2-none-any.whl",
        ("carbonara_archinfo", "7.7.9.14.post1", 'wheel'),
    ),
    ('pip-18.0-py2.py3-none-any.whl', ('pip', '18.0', 'wheel')),
    ('psycopg2-2.7.5-cp37-cp37m-macosx_10_6_intel.macosx_10_9_intel.macosx_10_9_x86_64.macosx_10_10_intel.macosx_10_10_x86_64.whl', ('psycopg2', '2.7.5', 'wheel')),
    ('psycopg2-2.7.5-cp37-cp37m-manylinux1_x86_64.whl', ('psycopg2', '2.7.5', 'wheel')),
    ('psycopg2-2.7.5-cp37-cp37m-win32.whl', ('psycopg2', '2.7.5', 'wheel')),
    (
        'pypi_simple-0.1.0.dev1-py2.py3-none-any.whl',
        ('pypi_simple', '0.1.0.dev1', 'wheel'),
    ),
    ('qypi-0.4.1-py3-none-any.whl', ('qypi', '0.4.1', 'wheel')),

    # wininst:
    ("1to001-0.2.0.win32.exe", ('1to001', '0.2.0', 'wininst')),
    ("4Suite-XML-1.0.1.win32-py2.2.exe", ('4Suite-XML', '1.0.1', 'wininst')),
    (
        "Appium-Python-Client-0.3.macosx-10.9-intel.exe",
        ("Appium-Python-Client", "0.3", 'wininst'),
    ),
    (
        "applicake-0.0.7.macosx-10.6-x86_64.exe",
        ('applicake', '0.0.7', 'wininst'),
    ),
    ("btk-0.3.0_win-amd64.exe", ('btk', '0.3.0', 'wininst')),
    ("btk-0.3.0_win32.exe", ('btk', '0.3.0', 'wininst')),
    ('l5x-1.2-win32.exe', ('l5x', '1.2', 'wininst')),
    (
        'pypi-simple-0.1.0.dev1.linux-x86_64.exe',
        ('pypi-simple', '0.1.0.dev1', 'wininst'),
    ),
    ('pytango-9.2.1.Win32-py2.7.exe', ('pytango', '9.2.1', 'wininst')),
    ("winappdbg-1.4.win-amd64.exe", ('winappdbg', '1.4', 'wininst')),

    # Invalid:
    ('500.tar.bz2', (None, None, None)),
    ('aa utility package-0.1.tar.gz', (None, None, None)),
    ('alexander.tar.gz', (None, None, None)),
    ('pip-18.0.tar.gz.txt', (None, None, None)),
    ('pip-18.0.txt', (None, None, None)),
    ('Pomodoro+-1.0.tar.gz', (None, None, None)),

    # Nonstandard oddities that may or may not be valid:
    pytest.param(
        "carbon-1.1.0_.tar.gz",
        ("carbon", "1.1.0", 'sdist'),
        marks=pytest.mark.xfail,
    ),
    pytest.param(
        "carbonara-archinfo-7.7.9.14-1.tar.gz",
        ("carbonara-archinfo", "7.7.9.14-1", 'sdist'),
        marks=pytest.mark.xfail,
    ),
    pytest.param(
        'psifas-0.3.msi',
        ('psifas', '0.3', 'msi'),
        marks=pytest.mark.xfail,
    ),
])
def test_parse_filename(filename, expected):
    assert parse_filename(filename) == expected
