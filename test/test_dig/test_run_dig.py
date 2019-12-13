import subprocess
import unittest
from unittest import mock
from unittest.mock import patch, call

import dig


class MyTestCase(unittest.TestCase):

    @patch.object(dig.DigResults, 'parse')
    @patch('subprocess.Popen')
    def test_basicRun(self, mock_subprocess_popen, mock_parse):
        parse_return = "Return 1"
        mock_parse.side_effect = [parse_return]

        process_mock = mock.Mock()
        attrs = {'communicate.return_value': (b'process output', b'process error')}
        process_mock.configure_mock(**attrs)

        mock_subprocess_popen.return_value = process_mock

        result = dig.run_dig("cnn.com", "1.1.1.1")
        self.assertEqual(parse_return, result)

        self.assertEqual(mock_subprocess_popen.call_count, 1)
        mock_subprocess_popen.assert_has_calls([call(["dig", "@1.1.1.1", "cnn.com", "+time=5", "+tries=1", "+stats"],
                                                     stdout=subprocess.PIPE)])

        self.assertEqual(mock_parse.call_count, 1)
        mock_parse.assert_has_calls([call('process output')])

    @patch.object(dig.DigResults, 'parse')
    @patch('subprocess.Popen')
    def test_noTarget(self, mock_subprocess_popen, mock_parse):
        parse_return = "Return 2"
        mock_parse.side_effect = [parse_return]

        process_mock = mock.Mock()
        attrs = {'communicate.return_value': (b'process output', b'process error')}
        process_mock.configure_mock(**attrs)

        mock_subprocess_popen.return_value = process_mock

        result = dig.run_dig("cnn.com")
        self.assertEqual(parse_return, result)

        self.assertEqual(mock_subprocess_popen.call_count, 1)
        mock_subprocess_popen.assert_has_calls([call(["dig", "cnn.com", "+time=5", "+tries=1", "+stats"],
                                                 stdout=subprocess.PIPE)])

        self.assertEqual(mock_parse.call_count, 1)
        mock_parse.assert_has_calls([call('process output')])

    @patch.object(dig.DigResults, 'parse')
    @patch('subprocess.Popen')
    def test_noStats(self, mock_subprocess_popen, mock_parse):
        parse_return = "Return 3"
        mock_parse.side_effect = [parse_return]

        process_mock = mock.Mock()
        attrs = {'communicate.return_value': (b'process output', b'process error')}
        process_mock.configure_mock(**attrs)

        mock_subprocess_popen.return_value = process_mock

        result = dig.run_dig("cnn.com", "1.1.1.42", stats=False)
        self.assertEqual(parse_return, result)

        self.assertEqual(mock_subprocess_popen.call_count, 1)
        mock_subprocess_popen.assert_has_calls([call(["dig", "@1.1.1.42", "cnn.com", "+time=5", "+tries=1"],
                                                 stdout=subprocess.PIPE)])

        self.assertEqual(mock_parse.call_count, 1)
        mock_parse.assert_has_calls([call('process output')])

    @patch.object(dig.DigResults, 'parse')
    @patch('subprocess.Popen')
    def test_includeNoRecurse(self, mock_subprocess_popen, mock_parse):
        parse_return = "Return 4"
        mock_parse.side_effect = [parse_return]

        process_mock = mock.Mock()
        attrs = {'communicate.return_value': (b'process output', b'process error')}
        process_mock.configure_mock(**attrs)

        mock_subprocess_popen.return_value = process_mock

        result = dig.run_dig("cnn.com", "1.1.42.1", norecurse=True)
        self.assertEqual(parse_return, result)

        self.assertEqual(mock_subprocess_popen.call_count, 1)
        mock_subprocess_popen.assert_has_calls([call(["dig", "@1.1.42.1", "cnn.com", "+time=5", "+tries=1", "+stats",
                                                      "+norecurse"], stdout=subprocess.PIPE)])

        self.assertEqual(mock_parse.call_count, 1)
        mock_parse.assert_has_calls([call('process output')])

    @patch.object(dig.DigResults, 'parse')
    @patch('subprocess.Popen')
    def test_alternateTimeAndTries(self, mock_subprocess_popen, mock_parse):
        process_mock = mock.Mock()
        attrs = {'communicate.return_value': (b'process output', b'process error')}
        process_mock.configure_mock(**attrs)

        mock_subprocess_popen.return_value = process_mock

        dig.run_dig("cnn.com", "1.1.1.1", time=42, tries=4242)

        self.assertEqual(mock_subprocess_popen.call_count, 1)
        mock_subprocess_popen.assert_has_calls([call(["dig", "@1.1.1.1", "cnn.com", "+time=42", "+tries=4242", "+stats"],
                                                     stdout=subprocess.PIPE)])

        self.assertEqual(mock_parse.call_count, 1)
        mock_parse.assert_has_calls([call('process output')])

    @patch.object(dig.DigResults, 'parse')
    @patch('subprocess.Popen')
    def test_attributeError(self, mock_subprocess_popen, mock_parse):
        mock_parse.side_effect = AttributeError()

        process_mock = mock.Mock()
        attrs = {'communicate.return_value': (b'process output', b'process error')}
        process_mock.configure_mock(**attrs)

        mock_subprocess_popen.return_value = process_mock

        self.assertRaises(Exception, dig.run_dig, "cnn.com", "1.1.1.1")

        self.assertEqual(mock_subprocess_popen.call_count, 1)
        mock_subprocess_popen.assert_has_calls([call(["dig", "@1.1.1.1", "cnn.com", "+time=5", "+tries=1", "+stats"],
                                                     stdout=subprocess.PIPE)])

        self.assertEqual(mock_parse.call_count, 1)
        mock_parse.assert_has_calls([call('process output')])
