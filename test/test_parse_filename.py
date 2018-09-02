import pytest
from   pypi_simple import parse_filename

#: Filenames that can be parsed correctly with or without a ``project_hint``
SIMPLE_FILENAMES = [
    # dumb:
    ("4ch-1.0.0.linux-x86_64.tar.gz", "4ch", ('4ch', '1.0.0', 'dumb')),
    (
        "AccelBrainBeat-1.0.0.win-amd64.zip",
        "AccelBrainBeat",
        ("AccelBrainBeat", "1.0.0", 'dumb'),
    ),
    (
        "Appengine-Fixture-Loader-0.1.8.linux-x86_64.tar.gz",
        "Appengine-Fixture-Loader",
        ("Appengine-Fixture-Loader", "0.1.8", 'dumb'),
    ),
    (
        "Appium-Python-Client-0.3.macosx-10.9-intel.tar.gz",
        "Appium-Python-Client",
        ("Appium-Python-Client", "0.3", 'dumb'),
    ),
    (
        'line.sep-0.2.0.dev1.linux-x86_64.tar.gz',
        'line.sep',
        ('line.sep', '0.2.0.dev1', 'dumb'),
    ),
    (
        'linesep-1.0.0.post1.linux-x86_64.tar.gz',
        'linesep',
        ('linesep', '1.0.0.post1', 'dumb'),
    ),
    (
        'pypi-simple-0.1.0.dev1.linux-x86_64.tar.gz',
        'pypi-simple',
        ('pypi-simple', '0.1.0.dev1', 'dumb'),
    ),

    # egg:
    (
        "4Suite_XML-1.0rc2-py2.5-win32-2.5.egg",
        '4Suite_XML',
        ('4Suite_XML', '1.0rc2', 'egg'),
    ),
    (
        "4Suite_XML-1.0.1-py2.5-win32.egg",
        '4Suite_XML',
        ('4Suite_XML', '1.0.1', 'egg')),
    (
        'Konnichiwa_Sekai-1!1.3.3-py3.6.egg',
        'Konnichiwa_Sekai',
        ('Konnichiwa_Sekai', '1!1.3.3', 'egg'),
    ),
    (
        'line.sep-0.2.0.dev1-py3.5.egg',
        'line.sep',
        ('line.sep', '0.2.0.dev1', 'egg'),
    ),
    # This is an actual anomaly in PyPI:
    ('munepy-1.3-py2.5.egg', 'flufl.enum', ('munepy', '1.3', 'egg')),
    (
        'pypi_simple-0.1.0.dev1-py3.5.egg',
        'pypi-simple',
        ('pypi_simple', '0.1.0.dev1', 'egg'),
    ),
    (
        'setuptools_scm-3.1.0-py2.7.egg',
        'setuptools_scm',
        ('setuptools_scm', '3.1.0', 'egg'),
    ),

    # msi:
    ('pyFAI-0.13.1.win-amd64-py2.7-1.msi', 'pyFAI', ('pyFAI', '0.13.1', 'msi')),
    (
        'pyOpenSSL-0.13.winxp32-py3.2.msi',
        'pyOpenSSL',
        ('pyOpenSSL', '0.13', 'msi'),
    ),
    ('pytango-9.2.0.Win32-py2.7.msi', 'pytango', ('pytango', '9.2.0', 'msi')),
    ("winappdbg-1.3.win32-py2.4.msi", 'winappdbg', ('winappdbg', '1.3', 'msi')),
    (
        "winappdbg-1.3.win-amd64-py2.4.msi",
        'winappdbg',
        ('winappdbg', '1.3', 'msi'),
    ),
    ("winappdbg-1.4.win32.msi", 'winappdbg', ('winappdbg', '1.4', 'msi')),
    ("winappdbg-1.4.win-amd64.msi", 'winappdbg', ('winappdbg', '1.4', 'msi')),

    # rpm:
    ("Aglyph-3.0.0-1.noarch.rpm", 'Agylph', ('Aglyph', '3.0.0', 'rpm')),
    ("Aglyph-3.0.0-1.src.rpm", 'Aglyph', ('Aglyph', '3.0.0', 'rpm')),
    ("anuga-1.3.1-1.x86_64.rpm", 'anuga', ('anuga', '1.3.1', 'rpm')),
    (
        "bootstrap_env-0.5.0-1.noarch.rpm",
        'bootstrap_env',
        ('bootstrap_env', '0.5.0', 'rpm'),
    ),
    ('Cheetah-2.2.2-1.x86_64.rpm', 'Cheetah', ('Cheetah', '2.2.2', 'rpm')),
    ('Cheetah-2.4.0-1.i586.rpm', 'Cheetah', ('Cheetah', '2.4.0', 'rpm')),
    (
        "clustershell-1.2-1.el5.noarch.rpm",
        'clustershell',
        ('clustershell', '1.2', 'rpm'),
    ),
    (
        'clustershell-1.2-1.fc11.noarch.rpm',
        'clustershell',
        ('clustershell', '1.2', 'rpm'),
    ),
    (
        'django-mako-0.1.4pre-1.noarch.rpm',
        'django-mako',
        ('django-mako', '0.1.4pre', 'rpm'),
    ),
    (
        'django-ssl-auth-0.8.2.1-126.sles11.noarch.rpm',
        'django-ssl-auth',
        ('django-ssl-auth', '0.8.2.1', 'rpm'),
    ),
    (
        'Flask-Celery-py3-0.2.1-1.noarch.rpm',
        'Flask-Celery-py3',
        ('Flask-Celery-py3', '0.2.1', 'rpm'),
    ),
    ('ipython-0.10-py25.noarch.rpm', 'iPython', ('ipython', '0.10', 'rpm')),
    (
        'libqutrub-python-1.0-3.1.noarch.rpm',
        'libqutrub-python',
        ('libqutrub-python', '1.0', 'rpm'),
    ),
    ("ll-core-1.2-1.i386.rpm", 'll-core', ('ll-core', '1.2', 'rpm')),
    ('LSystem2-1.3-1.pentium3.rpm', 'LSystem2', ('LSystem2', '1.3', 'rpm')),
    (
        'music_manager-0.1-0.1.noarch.rpm',
        'music_manager',
        ('music_manager', '0.1', 'rpm'),
    ),
    ('nml-0.1.1-suse1130.noarch.rpm', 'nml', ('nml', '0.1.1', 'rpm')),
    (
        'pyrasite-2.0-0.1.beta9.fc16.noarch.rpm',
        'pyrasite',
        ('pyrasite', '2.0', 'rpm'),
    ),
    ('pyspf-2.0.2-2.py24.noarch.rpm', 'pyspf', ('pyspf', '2.0.2', 'rpm')),
    (
        "python-turboflot-0.0.5-2.fc8.noarch.rpm",
        'TurboFloat',
        ('python-turboflot', '0.0.5', 'rpm'),
    ),
    (
        "python-turboflot-0.0.5-2.fc8.src.rpm",
        'TurboFloat',
        ('python-turboflot', '0.0.5', 'rpm'),
    ),
    (
        "python-turboflot-0.1.0-1.fc8.noarch.rpm",
        'TurboFloat',
        ('python-turboflot', '0.1.0', 'rpm'),
    ),
    (
        "python-turboflot-0.1.1-1.fc9.noarch.rpm",
        'TurboFlot',
        ('python-turboflot', '0.1.1', 'rpm'),
    ),
    (
        'txt2boil-b_v0.4.12-1.noarch.rpm',
        'txt2boil',
        ('txt2boil', 'b_v0.4.12', 'rpm'),
    ),

    # sdist:
    ("1-1.0.0.zip", '1', ('1', '1.0.0', 'sdist')),
    ("3-1-1.0.0.zip", '3-1', ('3-1', '1.0.0', 'sdist')),
    (
        "3color-Press-0.2.0.tar.bz2",
        '3color-Press',
        ('3color-Press', '0.2.0', 'sdist'),
    ),
    ("3to2_py3k-0.1b1.tar.gz", '3to2_py3k', ('3to2_py3k', '0.1b1', 'sdist')),
    ('amqplib-1.0.0.tgz', 'amqplib', ('amqplib', '1.0.0', 'sdist')),
    (
        "application_repository-0.1.post2.dev31171108.tar.gz",
        "application_repository",
        ("application_repository", "0.1.post2.dev31171108", 'sdist'),
    ),
    ('efilter-1!1.0.tar.gz', 'efilter', ('efilter', '1!1.0', 'sdist')),
    # This is an actual anomaly in PyPI:
    ('munepy-1.3.tar.gz', 'flufl.enum', ('munepy', '1.3', 'sdist')),
    (
        'line.sep-0.2.0.dev1.tar.gz',
        'line.sep',
        ('line.sep', '0.2.0.dev1', 'sdist'),
    ),
    ('pip-18.0.tar.gz', 'pip', ('pip', '18.0', 'sdist')),
    (
        'pypi-simple-0.1.0.dev1.tar.gz',
        'pypi-simple',
        ('pypi-simple', '0.1.0.dev1', 'sdist'),
    ),
    ('pytz-2008a.tar.bz2', 'pytz', ('pytz', '2008a', 'sdist')),
    ('setuptools-40.2.0.zip', 'setuptools', ('setuptools', '40.2.0', 'sdist')),

    # wheel:
    (
        "bencoder.pyx-1.1.2-pp226-pp226-win32.whl",
        "bencoder.pyx",
        ("bencoder.pyx", "1.1.2", 'wheel'),
    ),
    (
        "brotlipy-0.1.2-pp27-none-macosx_10_10_x86_64.whl",
        "brotlipy",
        ("brotlipy", "0.1.2", 'wheel'),
    ),
    (
        "brotlipy-0.3.0-pp226-pp226u-macosx_10_10_x86_64.whl",
        "brotlipy",
        ("brotlipy", "0.3.0", 'wheel'),
    ),
    (
        "carbonara_archinfo-7.7.9.14.post1-py2-none-any.whl",
        "carbonara_archinfo",
        ("carbonara_archinfo", "7.7.9.14.post1", 'wheel'),
    ),
    (
        'efilter-1!1.2-py2-none-any.whl',
        'efilter',
        ('efilter', '1!1.2', 'wheel'),
    ),
    (
        "line.sep-0.2.0.dev1-py2.py3-none-any.whl",
        "line.sep",
        ("line.sep", "0.2.0.dev1", 'wheel'),
    ),
    ('pip-18.0-py2.py3-none-any.whl', 'pip', ('pip', '18.0', 'wheel')),
    (
        'psycopg2-2.7.5-cp37-cp37m-macosx_10_6_intel.macosx_10_9_intel.macosx_10_9_x86_64.macosx_10_10_intel.macosx_10_10_x86_64.whl',
        'psycopg2',
        ('psycopg2', '2.7.5', 'wheel'),
    ),
    (
        'psycopg2-2.7.5-cp37-cp37m-manylinux1_x86_64.whl',
        'psycopg2',
        ('psycopg2', '2.7.5', 'wheel'),
    ),
    (
        'psycopg2-2.7.5-cp37-cp37m-win32.whl',
        'psycopg2',
        ('psycopg2', '2.7.5', 'wheel'),
    ),
    (
        'pypi_simple-0.1.0.dev1-py2.py3-none-any.whl',
        'pypi-simple',
        ('pypi_simple', '0.1.0.dev1', 'wheel'),
    ),
    ('qypi-0.4.1-py3-none-any.whl', 'qypi', ('qypi', '0.4.1', 'wheel')),

    # Seemingly invalid wheel filenames that pip accepts anyway:
    ("arq-0.3-py35+-none-any.whl", "arq", ("arq", "0.3", 'wheel')),
    (
        "astrocats-0.3.2-universal-none-any.whl",
        "astrocats",
        ("astrocats", "0.3.2", 'wheel'),
    ),
    (
        "bgframework-0.4-py2,py3,pypy-none-any.whl",
        "bgframework",
        ("bgframework", "0.4", 'wheel'),
    ),
    (
        "coremltools-0.3.0-py2.7-none-any.whl",
        "coremltools",
        ("coremltools", "0.3.0", 'wheel'),
    ),
    (
        "devtools-0.1-py35,py36-none-any.whl",
        "devtools",
        ("devtools", "0.1", 'wheel'),
    ),
    (
        "simple_workflow-0.1.47-pypy-none-any.whl",
        "simple_workflow",
        ("simple_workflow", "0.1.47", 'wheel'),
    ),
    (
        "SimpleSteem-1.1.9-3.0-none-any.whl",
        "SimpleSteem",
        ("SimpleSteem", "1.1.9", 'wheel'),
    ),

    # wininst:
    ("1to001-0.2.0.win32.exe", '1to001', ('1to001', '0.2.0', 'wininst')),
    (
        "4Suite-XML-1.0.1.win32-py2.2.exe",
        '4Suite-XML',
        ('4Suite-XML', '1.0.1', 'wininst'),
    ),
    (
        "Appium-Python-Client-0.3.macosx-10.9-intel.exe",
        "Appium-Python-Client",
        ("Appium-Python-Client", "0.3", 'wininst'),
    ),
    (
        "applicake-0.0.7.macosx-10.6-x86_64.exe",
        'applicake',
        ('applicake', '0.0.7', 'wininst'),
    ),
    (
        'line.sep-0.2.0.dev1.linux-x86_64.exe',
        'line.sep',
        ('line.sep', '0.2.0.dev1', 'wininst'),
    ),
    (
        'pypi-simple-0.1.0.dev1.linux-x86_64.exe',
        'pypi-simple',
        ('pypi-simple', '0.1.0.dev1', 'wininst'),
    ),
    (
        'pytango-9.2.1.Win32-py2.7.exe',
        'pytango',
        ('pytango', '9.2.1', 'wininst'),
    ),
    (
        "winappdbg-1.4.win-amd64.exe",
        'winappdbg',
        ('winappdbg', '1.4', 'wininst'),
    ),

    # Invalid:
    # Invalid package name:
    ('aa utility package-0.1.tar.gz', 'aa-utility-package', (None, None, None)),
    ('jvc-projector tools-0.1.tar.gz', 'jvc-projector-tools', (None, None, None)),
    ('Pomodoro+-1.0.tar.gz', 'Pomodoro', (None, None, None)),
    ('pypol_-0.2.linux-i686.exe', 'pypol2', (None, None, None)),
    ('pypol_-0.3.win32.exe', 'pypol2', (None, None, None)),
    ('pypol_-0.4.tar.gz', 'pypol2', (None, None, None)),
    ('pypol_-0.5-1.noarch.rpm', 'pypol2', (None, None, None)),
    ('pypol_-0.5-py2.6.egg', 'pypol2', (None, None, None)),
    ('qcodes_-0.1.0-py3-none-any.whl', 'qcodes', (None, None, None)),
    # Invalid version:
    (
        'AppValidationAutomation-0[1][1].1.tar.gz',
        'AppValidationAutomation',
        (None, None, None),
    ),
    ('caosz-1,0,0.tar.gz', 'caosz', (None, None, None)),
    ('CROC-1.0.60:61.tar.gz', 'CROC', (None, None, None)),
    ('Geraldo-0.2-alpha(5).tar.gz', 'Geraldo', (None, None, None)),
    ('limnoria-2013-01-21T20:33:09+0100.tar.gz', 'limnoria', (None, None, None)),
    ('Pegl-0.1a3~1.4.tar.gz', 'Pegl', (None, None, None)),
    ('pyjamas-0.8.1~+alpha1.tar.bz2', 'pyjamas', (None, None, None)),
    ('thrivext-0.0.3    .tar.gz', 'thrivext', (None, None, None)),
    # No version:
    ('500.tar.bz2', 'appwsgi', (None, None, None)),
    ('alexander.tar.gz', 'alexander', (None, None, None)),
    # Sdist with invalid name-version separator:
    ('appwsgi 667.tar.bz2', 'appwsgi', (None, None, None)),
    # Wheel without ABI tag:
    (
        "azure_iothub_service_client-1.1.0.0-py2-win32.whl",
        'azure-iothub-service-client',
        (None, None, None),
    ),
    # rpm with invalid release-architecture separator:
    ('btk-0.3.0-1_i686.rpm', 'btk', (None, None, None)),
    ('btk-0.3.0-1_x86_64.rpm', 'btk', (None, None, None)),
    # Egg with invalid pyver-platform separator:
    ('btk-0.3.0-py2.7_macosx-10.7-intel.egg', 'btk', (None, None, None)),
    # Wininst with invalid version-platform separator:
    ("btk-0.3.0_win32.exe", 'btk', (None, None, None)),
    ('l5x-1.2-win32.exe', 'l5x', (None, None, None)),
    # Invalid extension:
    ('pip-18.0.tar.gz.txt', 'pip', (None, None, None)),
    ('pip-18.0.txt', 'pip', (None, None, None)),
    # MSI without a platform:
    ('psifas-0.3.msi', 'psifas', (None, None, None)),
    # MSI with invalid version-platform separator:
    ('pyftpsync-1.1.0-win32.msi', 'pyftpsync', (None, None, None)),
    # Egg with hyphen in project name:
    ('pypi-simple-0.1.0.dev1-py3.5.egg', 'pypi-simple', (None, None, None)),
    # rpm without a release or architecture:
    ('streamtuner2-2.1.9_beta1.rpm', 'streamtuner2', (None, None, None)),
    ('streamtuner2-2.2.0.rpm', 'streamtuner2', (None, None, None)),
    # Sdist with invalid name-version separator:
    ('testmanager.1.1.1.tar.gz', 'TestManager', (None, None, None)),
    ('TestManager_1.2.0.tar.gz', 'TestManager', (None, None, None)),
    # Egg with too many components in pyver string:
    (
        'xrayutilities-1.4.0-py2.7.10-win-amd64.egg',
        'xrayutilities',
        (None, None, None),
    ),
]

@pytest.mark.parametrize('filename,expected', [
    (filename, expected) for filename, _, expected in SIMPLE_FILENAMES
])
def test_parse_filename_no_hint(filename, expected):
    assert parse_filename(filename) == expected

@pytest.mark.parametrize('filename,project_hint,expected', SIMPLE_FILENAMES + [
    ('apsw-3.8.2-r1.tar.gz', 'apsw', ('apsw', '3.8.2-r1', 'sdist')),
    ('apsw-3.8.2-r1.tar.gz', 'APSW', ('apsw', '3.8.2-r1', 'sdist')),
    (
        "carbonara-archinfo-7.7.9.14-1.tar.gz",
        "carbonara-archinfo",
        ("carbonara-archinfo", "7.7.9.14-1", 'sdist'),
    ),
    ('cbmpy-0.7.8-1.win-amd64.msi', 'cbmpy', ('cbmpy', '0.7.8-1', 'msi')),
    (
        'cx_Oracle-5.3-12c.win32-py3.4.exe',
        'cx_Oracle',
        ('cx_Oracle', '5.3-12c', 'wininst'),
    ),
    ('ddlib-2013-02-18.tar.gz', 'ddlib', ('ddlib', '2013-02-18', 'sdist')),
    ('walt-node-0.4-1.tar.gz', 'walt-node', ('walt-node', '0.4-1', 'sdist')),
    ('walt-node-0.4-1.tar.gz', 'walt.node', ('walt-node', '0.4-1', 'sdist')),
    ('walt-node-0.4-1.tar.gz', 'walt_node', ('walt-node', '0.4-1', 'sdist')),
    ('walt-node-0.4-1.tar.gz', 'WALT_NODE', ('walt-node', '0.4-1', 'sdist')),
    ('walt-node-0.4-1.tar.gz', 'WALT-._node', ('walt-node', '0.4-1', 'sdist')),
])
def test_parse_filename_project_hint(filename, project_hint, expected):
    assert parse_filename(filename, project_hint=project_hint) == expected
