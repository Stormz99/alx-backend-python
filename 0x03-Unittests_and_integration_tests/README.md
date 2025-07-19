# 0x03. Unittests and Integration Tests

## Description

This project focuses on writing unit and integration tests for Python functions and modules using the `unittest` framework and the `parameterized` library.

You will learn how to:
- Write unittests to validate functionality
- Test for exceptions
- Use mocks to isolate behavior
- Apply parameterized tests for cleaner test cases

## Tasks

- **Task 0:** Write parameterized tests for `access_nested_map` function.
- **Task 1:** Test `access_nested_map` with `KeyError` exceptions.
- **Task 2:** Use `@patch` to mock `requests.get` for testing an API call.
- **Task 3:** Integration test with `patch` to mock external services.

## Requirements

- All code is written in Python 3.7
- Follows `pycodestyle` (version 2.5)
- Includes docstrings for all modules, classes, and functions
- Test files are executable
- Test cases use `unittest` and `parameterized`

## Usage

Run a test file using:
```bash
./test_utils.py
