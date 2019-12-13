import os
import unittest
from dig import DigResults


def read_to_str(filename):
    filename = os.path.join(os.path.dirname(__file__), filename)
    with open(filename, 'r') as file:
        return file.read()


class MyTestCase(unittest.TestCase):
    def testParseEmpty(self):
        self.assertIsNone(DigResults.parse(''))

    def testParseNoServer(self):
        test_no_server = read_to_str('sample_dig_no_server.txt')
        self.assertIsNone(DigResults.parse(test_no_server))

    def testParseFull(self):
        test1 = read_to_str('sample_dig1.txt')
        result1 = DigResults.parse(test1)
        self.assertIsNotNone(result1)
        self.assertEqual(result1.query_time, 24)
        self.assertEqual(result1.msg_size, 143)
        self.assertEqual(result1.responding_server, "8.8.8.8")
        self.assertEqual(result1.AUTHORITY, 0)
        self.assertEqual(result1.ANSWER, 5)
        self.assertEqual(result1.ADDITIONAL, 1)
        self.assertEqual(result1.status, "NOERROR")
        self.assertEqual(result1.recursion_not_available, False)
        self.assertEqual(len(result1.additional_section), 0)
        self.assertEqual(len(result1.authority_section), 0)
        self.assertEqual(len(result1.answer_section), 5)

        self.assertEqual("status: NOERROR, query time: 24, message size: 143, responding server: 8.8.8.8, " +
                         "ANSWER: 5, AUTHORITY: 0, ADDITIONAL: 1" +
                         "\n\tANSWER section: ['[name: www.cnn.com., ttl: 261, class=IN, type=CNAME, ip=turner-tls.map.fastly.net.]', '[name: turner-tls.map.fastly.net., ttl: 29, class=IN, type=A, ip=151.101.1.67]', '[name: turner-tls.map.fastly.net., ttl: 29, class=IN, type=A, ip=151.101.65.67]', '[name: turner-tls.map.fastly.net., ttl: 29, class=IN, type=A, ip=151.101.129.67]', '[name: turner-tls.map.fastly.net., ttl: 29, class=IN, type=A, ip=151.101.193.67]']" +
                         "\n\tAUTHORITY section: []" +
                         "\n\tADDITIONAL section: []", str(result1))

    def testParseFullWithAuthority(self):
        test2 = read_to_str('sample_dig2.txt')
        result2 = DigResults.parse(test2)
        self.assertIsNotNone(result2)
        self.assertEqual(result2.query_time, 39)
        self.assertEqual(result2.msg_size, 236)
        self.assertEqual(result2.responding_server, "205.251.192.47")
        self.assertEqual(result2.AUTHORITY, 4)
        self.assertEqual(result2.ANSWER, 4)
        self.assertEqual(result2.ADDITIONAL, 1)
        self.assertEqual(result2.status, "NOERROR")
        self.assertEqual(result2.recursion_not_available, True)
        self.assertEqual(len(result2.additional_section), 0)
        self.assertEqual(len(result2.authority_section), 4)
        self.assertEqual(len(result2.answer_section), 4)

    def testParseFullWithAdditional(self):
        test3 = read_to_str('sample_dig3.txt')
        result3 = DigResults.parse(test3)
        self.assertIsNotNone(result3)
        self.assertEqual(result3.query_time, 68)
        self.assertEqual(result3.msg_size, 287)
        self.assertEqual(result3.responding_server, "192.5.6.30")
        self.assertEqual(result3.AUTHORITY, 4)
        self.assertEqual(result3.ANSWER, 1)
        self.assertEqual(result3.ADDITIONAL, 9)
        self.assertEqual(result3.status, "NOERROR")
        self.assertEqual(result3.recursion_not_available, False)
        self.assertEqual(len(result3.additional_section), 8)
        self.assertEqual(len(result3.authority_section), 4)
        self.assertEqual(len(result3.answer_section), 1)
