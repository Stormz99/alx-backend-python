#!/usr/bin/env python3
"""
Unit tests for utils.py functions.
"""

import unittest
from parameterized import parameterized
from unittest.mock import patch, Mock
from utils import access_nested_map, get_json, memoize
import requests


class TestAccessNestedMap(unittest.TestCase):
    """Test cases for access_nested_map."""

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
        """Test access_nested_map raises KeyError"""
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        self.assertEqual(str(cm.exception), f"'{expected_key}'")


class TestGetJson(unittest.TestCase):
    """Test cases for get_json."""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"data": "value"}),
    ])
    @patch("utils.requests.get")
    def test_get_json(self, url, expected, mock_get):
        """Test get_json returns correct result from mocked requests.get"""
        mock_response = Mock()
        mock_response.json.return_value = expected
        mock_get.return_value = mock_response

        self.assertEqual(get_json(url), expected)
        mock_get.assert_called_once_with(url)


class TestMemoize(unittest.TestCase):
    """Test case for memoize decorator."""

    def test_memoize(self):
        """Test memoize decorator."""
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        obj = TestClass()

        with patch.object(obj, "a_method") as mock_method:
            mock_method.return_value = 42
            self.assertEqual(obj.a_property, 42)
            self.assertEqual(obj.a_property, 42)
            mock_method.assert_called_once()


if __name__ == "__main__":
    unittest.main()
