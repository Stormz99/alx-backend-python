#!/usr/bin/env python3
"""
This module contains unit tests for functions in the utils module.
"""

import unittest
from parameterized import parameterized
from unittest.mock import patch, Mock
from utils import access_nested_map, get_json


class TestAccessNestedMap(unittest.TestCase):
    """
    Unit test class for the `access_nested_map` function in utils.py.
    """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test access_nested_map returns correct value"""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), 'a'),
        ({"a": 1}, ("a", "b"), 'b'),
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected_key):
        """Test access_nested_map raises KeyError for missing keys"""
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        self.assertEqual(str(cm.exception), f"'{expected_key}'")


class TestGetJson(unittest.TestCase):
    """
    Unit test class for the `get_json` function in utils.py.
    """

    @parameterized.expand([
        ("https://example.com", {"payload": True}),
        ("https://api.github.com", {"data": "value"}),
    ])
    @patch("utils.requests.get")
    def test_get_json(self, url, expected, mock_get):
        """Test get_json returns expected result with mocked requests.get"""
        mock_response = Mock()
        mock_response.json.return_value = expected
        mock_get.return_value = mock_response

        result = get_json(url)
        self.assertEqual(result, expected)
        mock_get.assert_called_once_with(url)


if __name__ == "__main__":
    unittest.main()
