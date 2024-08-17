

import pytest

def add(x, y):
    return x + y

def test_add():
    assert add(2, 3) == 5 # basic test case
    assert add(-5, 10) == 5 # negative numbers
    assert add(0, 0) == 0 # edge case: adding two zeros
    assert add(2.5, 3.5) == 6 # decimal numbers
    assert add("Hello", "World") == "HelloWorld" # string concatenation
    assert add([1, 2, 3], [4, 5, 6]) == [1, 2, 3, 4, 5, 6] # adding lists
    assert add(2, "3") == "23" # edge case: adding integer and string
    assert add(2, None) == None # edge case: adding integer and NoneType