import unittest
from unittest import mock
from unittest.mock import patch
from datetime import datetime

import requests
from apis.tiingo_api import TiingoAPI


class TestTiingoAPI(unittest.TestCase):
    def setUp(self):
        self.api = TiingoAPI("my_api_key")

    @patch.object(TiingoAPI, "build_download_url")
    @patch.object(TiingoAPI, "make_request_with_retry")
    def test_download_ticker_success(self, mock_make_request, mock_build_url):
        """Test successful download of ticker data."""
        mock_build_url.return_value = "http://example.com/data"
        mock_make_request.return_value = "csv_data"

        result = self.api.download_ticker(
            "AAPL",
            datetime(2022, 1, 1),
            datetime(2022, 1, 2),
            15,
            False
        )

        mock_build_url.assert_called_once_with(
            "AAPL",
            datetime(2022, 1, 1),
            datetime(2022, 1, 2),
            15,
            False
        )
        mock_make_request.assert_called_once_with("http://example.com/data")
        self.assertEqual(result, "csv_data")

    @patch.object(TiingoAPI, "build_download_url")
    @patch.object(TiingoAPI, "make_request_with_retry")
    def test_download_ticker_404_error(self, mock_make_request, mock_build_url):
        """Test handling of 404 error during download."""
        mock_build_url.return_value = "http://example.com/data"
        mock_make_request.side_effect = requests.exceptions.HTTPError(
            response=mock.Mock(status_code=404)
        )

        result = self.api.download_ticker(
            "AAPL",
            datetime(2022, 1, 1),
            datetime(2022, 1, 2),
            15,
            False
        )

        mock_build_url.assert_called_once_with(
            "AAPL",
            datetime(2022, 1, 1),
            datetime(2022, 1, 2),
            15,
            False
        )
        mock_make_request.assert_called_once_with("http://example.com/data")
        self.assertIsNone(result)

    @patch.object(TiingoAPI, "build_download_url")
    @patch.object(TiingoAPI, "make_request_with_retry")
    def test_download_ticker_request_exception(self, mock_make_request, mock_build_url):
        """Test handling of request exception during download."""
        mock_build_url.return_value = "http://example.com/data"
        mock_make_request.side_effect = requests.exceptions.RequestException

        with self.assertRaises(requests.exceptions.RequestException):
            self.api.download_ticker(
                "AAPL",
                datetime(2022, 1, 1),
                datetime(2022, 1, 2),
                15,
                False
            )

        mock_build_url.assert_called_once_with(
            "AAPL",
            datetime(2022, 1, 1),
            datetime(2022, 1, 2),
            15,
            False
        )
        mock_make_request.assert_called_once_with("http://example.com/data")
