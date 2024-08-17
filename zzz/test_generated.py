
import pytest

def test_add():
    assert add(2, 3) == 5
    assert add(-2, 5) == 3
    assert add(0, 0) == 0
    assert add(10, -10) == 0
    assert add(2.5, 3.5) == 6.0