import unittest
from unittest.mock import patch, MagicMock
import Front_end

class TestFrontEnd(unittest.TestCase):

    @patch('Front_end.back.initial_read')
    def test_load_data_from_csv(self, mock_initial_read):
        mock_initial_read.return_value = [{"id": "1", "name": "Test", "description": "Test description"}]
        data = Front_end.load_data_from_csv()
        self.assertEqual(data, [{"id": "1", "name": "Test", "description": "Test description"}])

    @patch('Front_end.messagebox.showwarning')
    @patch('Front_end.tree.selection')
    def test_view_details_no_selection(self, mock_selection, mock_showwarning):
        mock_selection.return_value = []
        Front_end.view_details()
        mock_showwarning.assert_called_with("Error", "Please select an item to view details.")

    @patch('Front_end.tree.selection')
    @patch('Front_end.tree.item')
    @patch('Front_end.show_item_details')
    def test_view_details_with_selection(self, mock_show_item_details, mock_item, mock_selection):
        mock_selection.return_value = ['item1']
        mock_item.return_value = {"values": ("Test Name", "2025-03-13", "Test Album")}
        Front_end.sample_data = [{"id": "1", "name": "Test Name", "description": "Test description", "releasedate": "2025-03-13", "albumtitle": "Test Album"}]
        Front_end.view_details()
        mock_show_item_details.assert_called_once()

    def test_validate_register(self):
        self.assertFalse(Front_end.validate_register("", "password"))
        self.assertFalse(Front_end.validate_register("username", ""))
        self.assertTrue(Front_end.validate_register("username", "password"))

    @patch('Front_end.open', create=True)
    def test_is_username_taken(self, mock_open):
        mock_open.return_value.__enter__.return_value = MagicMock(read=lambda: "user1,password1\nuser2,password2\n")
        self.assertTrue(Front_end.is_username_taken("user1"))
        self.assertFalse(Front_end.is_username_taken("user3"))

    def test_validate_inputs(self):
        Front_end.sample_data = [{"id": "1", "name": "Test", "description": "Test description"}]
        self.assertFalse(Front_end.validate_inputs("", "name", "description"))
        self.assertFalse(Front_end.validate_inputs("1", "name", "description"))
        self.assertTrue(Front_end.validate_inputs("2", "name", "description"))

if __name__ == '__main__':
    unittest.main()