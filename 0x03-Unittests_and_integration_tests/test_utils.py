#!/usr/bin/env python3
"""
This module contains unit tests for the `access_nested_map` function
in the utils module.
"""

import unittest
from parameterized import parameterized
from utils import access_nested_map
from unittest.mock import patch, Mock
import requests



class TestAccessNestedMap(unittest.TestCase):
    """
    Unit test class for the `access_nested_map` function in utils.py.
    """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(
        self,
        nested_map: dict,
        path: tuple,
        expected: object
    ) -> None:
        """
        Test that access_nested_map returns correct value
        for given nested map and key path.
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), 'a'),
        ({"a": 1}, ("a", "b"), 'b')
    ])
    def test_access_nested_map_exception(
        self,
        nested_map: dict,
        path: tuple,
        expected_key: str
    ) -> None:
        """
        Test that KeyError is raised when accessing missing key.
        """
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        self.assertEqual(str(cm.exception), f"'{expected_key}'")

    def get_json(url):
        response = requests.get(url)
        return response.json()


        result = get_json(url)
        self.assertEqual(result, expected)
        mock_get.assert_called_once_with(url)
        
    @parameterized.expand([
        ("https://example.com", {"payload": True}),
        ("https://api.github.com", {"data": "value"}),
    ])
    @patch('utils.requests.get')
    def test_get_json(self, url: str, expected: dict, mock_get: Mock) -> None:
        """
        Test that get_json returns correct JSON response using mocked requests.get
        """
        mock_response = Mock()
        mock_response.json.return_value = expected
        mock_get.return_value = mock_response
        
        from utils import get_json
        result = get_json(url)
        self.assertEqual(result, expected)
        # Ensure that requests.get was called with the correct URL
        mock_get.assert_called_once_with(url)





if __name__ == "__main__":
    unittest.main()
