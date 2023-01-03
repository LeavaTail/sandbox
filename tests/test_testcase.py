"""Unit test for testcase.py 

testcase class method verification
* each setter can be set
* lookup *.notrun is success/failed
"""

import os
import pytest
from logging import getLogger, CRITICAL
from viewer.testcase import PassedClass, SkippedClass, FailedClass

getLogger("__main__").setLevel(CRITICAL)

@pytest.fixture(scope='module', autouse=True)
def module_fixture():
    """Prepare the xfstests results directory

    SkippedClass lookup *.notrun file to input the reason why the test
    will be skipped. To verify lookup sequence, create the simple results
    directory. (`dir/foo.notrun`)
    """
    # Set up process
    os.mkdir('dir')
    with open('dir/foo.notrun', mode='x') as f:
        f.write('sample')

    # Main process
    yield

    # Clean up process
    os.remove('dir/foo.notrun')
    os.rmdir('dir')

# PassedClass constructor will set `name`
def test_passed1():
    target = PassedClass('foo')
    assert target.name == 'foo'

# PassedClass update_time() will set `sec`
def test_passed2():
    target = PassedClass('foo')
    target.update_time(100)
    assert target.sec == 100

# PassedClass update_summary() will be noop
def test_passed3():
    target = PassedClass('foo')
    target.update_summary('bar')
    assert target.remarks == ''

# PassedClass update_path() will set `path`
def test_passed4():
    target = PassedClass('foo')
    target.update_path('path')
    assert target.path == 'path/foo'

# SkippedClass constructor will set `name`
def test_skipped1():
    target = SkippedClass('foo')
    assert target.name == 'foo'

# SkippedClass update_time() will set `sec`
def test_skipped2():
    target = SkippedClass('foo')
    target.update_time(100)
    assert target.sec == 100

# SkippedClass update_summary() will set `remarks` if file is exist
def test_skipped3():
    target = SkippedClass('foo')
    target.update_summary('dir/')
    assert target.remarks == 'sample'

# SkippedClass update_summary() will raise exception if file is not exist
def test_skipped4():
    target = SkippedClass('bar')
    with pytest.raises(SystemExit):
        target.update_summary('dir/')

# SkippedClass update_path() will set `path`
def test_skipped5():
    target = SkippedClass('foo')
    target.update_path('dir')
    assert target.path == 'dir/foo'

# FailedClass constructor will set `name`
def test_failed1():
    target = FailedClass('foo')
    assert target.name == 'foo'

# FailedClass update_time() will set `sec`
def test_failed2():
    target = FailedClass('foo')
    target.update_time(100)
    assert target.sec == 100

# FailedClass update_summary() will be noop
def test_failed3():
    target = FailedClass('foo')
    target.update_summary('bar')
    assert target.remarks == ''

# FailedClass update_path() will set `path`
def test_failed4():
    target = FailedClass('foo')
    target.update_path('path')
    assert target.path == 'path/foo'
