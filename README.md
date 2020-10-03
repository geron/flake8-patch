# flake8-patch

A `flake8` plugin checking for mocking issues.

Currently reports the code `PAT001` when assignments to imported objects are detected.

## Bad code example

```python
from some_module import SomeClass

def test_something():
    SomeClass.some_method = lambda: 42
```

This is bad because `SomeClass.some_method` might be used directly or indirectly in another test, which will break randomly depending on the execution order.

## Good code example

```python
from some_module import SomeClass

def test_something(mocker):
    mocker.patch.object(SomeClass, "some_method", return_value=42)
```

This uses the mocker fixture from `pytest-mock` to automatically unwind the patch after the test method runs.

## Change Log

**Unreleased**

Add PAT001: assignment to imported name
