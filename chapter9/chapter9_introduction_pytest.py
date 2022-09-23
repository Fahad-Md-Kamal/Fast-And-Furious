
from chapter9.chapter9_introduction import add


def test_add():
    assert add(2,3) == 5
    assert add(0,0) == 0
    assert add(100,0) == 100
    assert add(1,1) == 2
