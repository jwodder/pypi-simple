from pypi_simple import parse_links

def test_basic():
    assert list(parse_links('''
<html>
<head><title>Basic test</title></head>
<body>
<a href="one.html">link1</a>
<a href="two.html">link-two</a>
<span href="zero.html">not-a-link</span>
</body>
</html>
'''
    )) == [
        ('link1', 'one.html', {'href': 'one.html'}),
        ('link-two', 'two.html', {'href': 'two.html'}),
    ]

def test_base_url():
    assert list(parse_links('''
<html>
<head><title>Test with base_url</title></head>
<body>
<a href="one.html">link1</a>
<a href="two.html">link-two</a>
<span href="zero.html">not-a-link</span>
</body>
</html>
''', base_url='https://test.nil/base/'
    )) == [
        ('link1', 'https://test.nil/base/one.html', {'href': 'one.html'}),
        ('link-two', 'https://test.nil/base/two.html', {'href': 'two.html'}),
    ]

def test_base_tag():
    assert list(parse_links('''
<html>
<head>
    <title>Test with &lt;base&gt; tag</title>
    <base href="https://nil.test/path/"/>
</head>
<body>
<a href="one.html">link1</a>
<a href="two.html">link-two</a>
<span href="zero.html">not-a-link</span>
</body>
</html>
'''
    )) == [
        ('link1', 'https://nil.test/path/one.html', {'href': 'one.html'}),
        ('link-two', 'https://nil.test/path/two.html', {'href': 'two.html'}),
    ]

def test_base_url_and_absolute_base_tag():
    assert list(parse_links('''
<html>
<head>
    <title>Test with both base_url and an absolute &lt;base&gt; tag</title>
    <base href="https://nil.test/path/"/>
</head>
<body>
<a href="one.html">link1</a>
<a href="two.html">link-two</a>
<span href="zero.html">not-a-link</span>
</body>
</html>
''', base_url='https://test.nil/base/'
    )) == [
        ('link1', 'https://nil.test/path/one.html', {'href': 'one.html'}),
        ('link-two', 'https://nil.test/path/two.html', {'href': 'two.html'}),
    ]

def test_base_url_and_relative_base_tag():
    assert list(parse_links('''
<html>
<head>
    <title>Test with both base_url and a relative &lt;base&gt; tag</title>
    <base href="subdir/"/>
</head>
<body>
<a href="one.html">link1</a>
<a href="two.html">link-two</a>
<span href="zero.html">not-a-link</span>
</body>
</html>
''', base_url='https://test.nil/base/'
    )) == [
        ('link1', 'https://test.nil/base/subdir/one.html', {'href': 'one.html'}),
        ('link-two', 'https://test.nil/base/subdir/two.html', {'href': 'two.html'}),
    ]

def test_uppercase():
    assert list(parse_links('''
<html>
<head>
    <title>Test with uppercase tags &amp; attributes</title>
    <BASE HREF="https://nil.test/path/"/>
</head>
<body>
<A HREF="one.html">link1</a>
<A HREF="two.html">link-two</A>
<span href="zero.html">not-a-link</span>
</body>
</html>
'''
    )) == [
        ('link1', 'https://nil.test/path/one.html', {'href': 'one.html'}),
        ('link-two', 'https://nil.test/path/two.html', {'href': 'two.html'}),
    ]
