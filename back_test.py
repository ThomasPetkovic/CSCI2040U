import pytest
from unittest.mock import patch, mock_open, call
from back import initial_read, rewrite_csv

def test_initial_read():
    mock_file_data = "name,description,id,albumtitle,genre,releasedate\nSong A,First song,1,Album X,Pop,2021\nSong B,Second song,2,Album Y,Rock,2022\n"
    with patch("builtins.open", mock_open(read_data=mock_file_data)):
        assert initial_read() == [
            {"name": "Song A", "description": "First song", "id": "1", "albumtitle": "Album X", "genre": "Pop", "releasedate": "2021"},
            {"name": "Song B", "description": "Second song", "id": "2", "albumtitle": "Album Y", "genre": "Rock", "releasedate": "2022"},
        ]

def test_rewrite_csv():
    mock_file_data = ""
    mock_list = [
        {"name": "Song A", "description": "First song", "id": "1", "albumtitle": "Album X", "genre": "Pop", "releasedate": "2021"},
        {"name": "Song B", "description": "Second song", "id": "2", "albumtitle": "Album Y", "genre": "Rock", "releasedate": "2022"},
    ]
    expected_output = [
        call("name,description,id,albumtitle,genre,releasedate\r\n"),
        call("Song A,First song,1,Album X,Pop,2021\r\n"),
        call("Song B,Second song,2,Album Y,Rock,2022\r\n")
    ]
    with patch("builtins.open", mock_open(read_data=mock_file_data)) as mock_file:
        rewrite_csv(mock_list)
        mock_file.assert_called_with("test.csv", mode="w", newline="")
        mock_file().write.assert_has_calls(expected_output, any_order=False)