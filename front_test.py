import pytest
from unittest.mock import patch, mock_open
from front_end import validate_register, validate_login, validate_inputs, search_item, is_username_taken
from tkinter import messagebox
from unittest.mock import patch, MagicMock


#Test to see if the registration is working properly
@patch.object(messagebox, "showwarning")
@patch.object(messagebox, "showinfo")
@patch.object(messagebox, "showerror")
def test_validate_register(mock_showerror, mock_showinfo, mock_showwarning):
    assert validate_register("user", "pass") is True
    assert validate_register("", "pass") is False
    assert validate_register("user", "") is False
    assert validate_register("", "") is False


#Test to see if the login is working properly
@patch.object(messagebox, "showwarning")
@patch.object(messagebox, "showinfo")
@patch.object(messagebox, "showerror")
def test_validate_login(mock_showerror, mock_showinfo, mock_showwarning):
    assert validate_login("user", "pass") is True           

    #Edge cases    
    assert validate_login("", "pass") is False
    assert validate_login("user", "") is False
    assert validate_login("", "") is False

#Test to see if the input is working and all fields are complete and ID is numeric
@patch.object(messagebox, "showwarning")
@patch.object(messagebox, "showinfo")
@patch.object(messagebox, "showerror")
def test_validate_inputs(mock_showerror, mock_showinfo, mock_showwarning):

    #Empty fields should fail.
    assert validate_inputs("", "Song Name", "A cool song") is False
    assert validate_inputs("1", "", "A cool song") is False
    assert validate_inputs("1", "Song Name", "") is False

    #ID must be numeric
    assert validate_inputs("abc", "Song Name", "A cool song") is False 


##Test to see if the username is already taken.
@patch.object(messagebox, "showwarning")
@patch.object(messagebox, "showinfo")
@patch.object(messagebox, "showerror")
def test_is_username_taken(mock_showerror, mock_showinfo, mock_showwarning):

    #Simulate opening a file with users to test username taken functionality
    mock_file_data = "user1,password1\nuser2,password2\n"
    with patch("builtins.open", mock_open(read_data=mock_file_data)):
        assert is_username_taken("user1") is True
        assert is_username_taken("user2") is True
        assert is_username_taken("user3") is False

    #If the username is not found in file, then no username is taken.
    with patch("builtins.open", side_effect=FileNotFoundError()):
        assert is_username_taken("user1") is False