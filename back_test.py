import unittest
from unittest.mock import mock_open, patch
from back import initial_read, rewrite_csv

# test_back.py


class TestBackFunctions(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open, read_data="name,description,id,albumtitle,genre,releasedate\nJohn Doe,Sample Description,1,Sample Album,Rock,2021-01-01")
    def test_initial_read(self, mock_file):
        expected_output = [
            {
                "name": "John Doe",
                "description": "Sample Description",
                "id": "1",
                "albumtitle": "Sample Album",
                "genre": "Rock",
                "releasedate": "2021-01-01"
            }
        ]
        result = initial_read()
        self.assertEqual(result, expected_output)
        mock_file.assert_called_once_with("test.csv", mode="r")

    @patch("builtins.open", new_callable=mock_open)
    def test_rewrite_csv(self, mock_file):
        data = [
            {
                "name": "John Doe",
                "description": "Sample Description",
                "id": "1",
                "albumtitle": "Sample Album",
                "genre": "Rock",
                "releasedate": "2021-01-01"
            }
        ]
        rewrite_csv(data)
        mock_file.assert_called_once_with("test.csv", mode="w", newline="")
        handle = mock_file()
        handle.write.assert_any_call("name,description,id,albumtitle,genre,releasedate\r\n")
        handle.write.assert_any_call("John Doe,Sample Description,1,Sample Album,Rock,2021-01-01\r\n")

if __name__ == "__main__":
    unittest.main()