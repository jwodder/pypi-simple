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
