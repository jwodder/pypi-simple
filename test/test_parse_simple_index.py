from os.path     import dirname, join
from pypi_simple import PYPI_SIMPLE_ENDPOINT, parse_simple_index

DATA_DIR = join(dirname(__file__), 'data')

def test_empty():
    assert list(parse_simple_index('', PYPI_SIMPLE_ENDPOINT)) == []

def test_simple01():
    with open(join(DATA_DIR, 'simple01.html'), 'rb') as fp:
        assert list(parse_simple_index(
            fp.read(),
            PYPI_SIMPLE_ENDPOINT,
            from_encoding='utf-8',
        )) == [
            ('a', PYPI_SIMPLE_ENDPOINT + 'a/'),
            ('a00k5pgrtn', PYPI_SIMPLE_ENDPOINT + 'a00k5pgrtn/'),
            ('a10ctl', PYPI_SIMPLE_ENDPOINT + 'a10ctl/'),
            ('a10-horizon', PYPI_SIMPLE_ENDPOINT + 'a10-horizon/'),
            ('a10-neutronclient', PYPI_SIMPLE_ENDPOINT + 'a10-neutronclient/'),
            ('a10-neutron-lbaas', PYPI_SIMPLE_ENDPOINT + 'a10-neutron-lbaas/'),
            ('a10-openstack-lbaas', PYPI_SIMPLE_ENDPOINT + 'a10-openstack-lbaas/'),
            ('a10-openstack-lib', PYPI_SIMPLE_ENDPOINT + 'a10-openstack-lib/'),
            ('a10sdk', PYPI_SIMPLE_ENDPOINT + 'a10sdk/'),
            ('a2d_diary', PYPI_SIMPLE_ENDPOINT + 'a2d-diary/'),
            ('a2m.itertools', PYPI_SIMPLE_ENDPOINT + 'a2m-itertools/'),
            ('a2p2', PYPI_SIMPLE_ENDPOINT + 'a2p2/'),
            ('a2pcej', PYPI_SIMPLE_ENDPOINT + 'a2pcej/'),
            ('a2svm', PYPI_SIMPLE_ENDPOINT + 'a2svm/'),
            ('a2w', PYPI_SIMPLE_ENDPOINT + 'a2w/'),
            ('a2x', PYPI_SIMPLE_ENDPOINT + 'a2x/'),
            ('a318288f-60c1-4176-a6be-f8a526b27661', PYPI_SIMPLE_ENDPOINT + 'a318288f-60c1-4176-a6be-f8a526b27661/'),
            ('A3MIO', PYPI_SIMPLE_ENDPOINT + 'a3mio/'),
            ('a3rt-sdk-py', PYPI_SIMPLE_ENDPOINT + 'a3rt-sdk-py/'),
            ('a4t-party_contact', PYPI_SIMPLE_ENDPOINT + 'a4t-party-contact/'),
        ]

def test_simple_base():
    with open(join(DATA_DIR, 'simple_base.html'), 'rb') as fp:
        assert list(parse_simple_index(
            fp.read(),
            PYPI_SIMPLE_ENDPOINT,
            from_encoding='utf-8',
        )) == [
            ('a', PYPI_SIMPLE_ENDPOINT + 'projects/a/'),
            ('a00k5pgrtn', PYPI_SIMPLE_ENDPOINT + 'projects/a00k5pgrtn/'),
            ('a10ctl', PYPI_SIMPLE_ENDPOINT + 'projects/a10ctl/'),
            ('a10-horizon', PYPI_SIMPLE_ENDPOINT + 'projects/a10-horizon/'),
            ('a10-neutronclient', PYPI_SIMPLE_ENDPOINT + 'projects/a10-neutronclient/'),
        ]

def test_simple_devpi():
    with open(join(DATA_DIR, 'simple_devpi.html'), 'rb') as fp:
        assert list(parse_simple_index(
            fp.read(),
            'https://m.devpi.net/fschulze/dev/+simple/',
            from_encoding='utf-8',
        )) == [
            ('devpi', 'https://m.devpi.net/fschulze/dev/+simple/devpi'),
            ('devpi-client', "https://m.devpi.net/fschulze/dev/+simple/devpi-client"),
            ('devpi-common', "https://m.devpi.net/fschulze/dev/+simple/devpi-common"),
            ('devpi-jenkins', "https://m.devpi.net/fschulze/dev/+simple/devpi-jenkins"),
            ('devpi-ldap', "https://m.devpi.net/fschulze/dev/+simple/devpi-ldap"),
            ('devpi-lockdown', "https://m.devpi.net/fschulze/dev/+simple/devpi-lockdown"),
            ('devpi-postgresql', "https://m.devpi.net/fschulze/dev/+simple/devpi-postgresql"),
            ('devpi-server', "https://m.devpi.net/fschulze/dev/+simple/devpi-server"),
            ('devpi-web', "https://m.devpi.net/fschulze/dev/+simple/devpi-web"),
            ('ploy-ezjail', "https://m.devpi.net/fschulze/dev/+simple/ploy-ezjail"),
            ('pytest', "https://m.devpi.net/fschulze/dev/+simple/pytest"),
            ('waitress', "https://m.devpi.net/fschulze/dev/+simple/waitress"),
            ('0', "https://m.devpi.net/fschulze/dev/+simple/0"),
            ('0-0', "https://m.devpi.net/fschulze/dev/+simple/0-0"),
            ('0-0-1', "https://m.devpi.net/fschulze/dev/+simple/0-0-1"),
            ('0-core-client', "https://m.devpi.net/fschulze/dev/+simple/0-core-client"),
            ('0-orchestrator', "https://m.devpi.net/fschulze/dev/+simple/0-orchestrator"),
            ('00smalinux', "https://m.devpi.net/fschulze/dev/+simple/00smalinux"),
        ]
