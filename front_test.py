import pytest
from unittest.mock import patch, mock_open
from front_end import validate_register, validate_login, validate_inputs, search_item, is_username_taken

def test_validate_register():
    assert validate_register("user", "pass") is True
    assert validate_register("", "pass") is False  # Username cannot be empty
    assert validate_register("user", "") is False  # Password cannot be empty
    assert validate_register("", "") is False  # Both fields cannot be empty

def test_validate_login():
    assert validate_login("user", "pass") is True
    assert validate_login("", "pass") is False  # Username cannot be empty
    assert validate_login("user", "") is False  # Password cannot be empty
    assert validate_login("", "") is False  # Both fields cannot be empty

def test_validate_inputs():
    assert validate_inputs("", "Song Name", "A cool song") is False  # ID cannot be empty
    assert validate_inputs("1", "", "A cool song") is False  # Name cannot be empty
    assert validate_inputs("1", "Song Name", "") is False  # Description cannot be empty
    assert validate_inputs("abc", "Song Name", "A cool song") is False  # ID must be numeric
    assert validate_inputs("1", "Song Name", "A cool song") is True  # Valid input

def test_is_username_taken():
    mock_file_data = "user1,password1\nuser2,password2\n"
    
    # Simulate reading from a user file
    with patch("builtins.open", mock_open(read_data=mock_file_data)):
        assert is_username_taken("user1") is True  # User exists
        assert is_username_taken("user2") is True  # User exists
        assert is_username_taken("user3") is False  # User does not exist

    # Simulate file not found case
    with patch("builtins.open", side_effect=FileNotFoundError()):
        assert is_username_taken("user1") is False  # If file is missing, assume user does not exist

@pytest.fixture
def mock_sample_data():
    return [
        {"id": "1", "name": "Song A", "description": "First song", "releasedate": "2021", "albumtitle": "Album X"},
        {"id": "2", "name": "Song B", "description": "Second song", "releasedate": "2022", "albumtitle": "Album Y"},
    ]

def test_search_item(mock_sample_data, monkeypatch):
    # Simulate global variables in front_end module
    global sample_data, tree
    sample_data = mock_sample_data

    # Mocking Tkinter treeview
    class MockTree:
        def get_children(self):
            return []
        def delete(self, x):
            pass
        def insert(self, *args):
            pass

    tree = MockTree()
    
    # Mocking search input field
    class MockEntry:
        def __init__(self, text):
            self.text = text
        def get(self):
            return self.text

    # Test search with an existing song
    monkeypatch.setattr("front_end.search_entry", MockEntry("Song A"))
    search_item()  # Should find "Song A"

    # Test search with a non-existent song
    monkeypatch.setattr("front_end.search_entry", MockEntry("Nonexistent"))
    search_item()  # Should result in an error message
