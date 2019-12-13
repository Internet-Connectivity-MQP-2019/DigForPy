import unittest
from dig import DigSectionLine


class TestDigMethods(unittest.TestCase):

    def testParseEmptyLine(self):
        self.assertIsNone(DigSectionLine.parse(''))

    def testParseLine(self):
        line1 = "cnn.com.                14      IN      A       151.101.193.67"
        parsed1 = DigSectionLine.parse(line1)
        self.assertEqual(parsed1.name, "cnn.com.")
        self.assertEqual(parsed1.ttl, 14)
        self.assertEqual(parsed1.response_class, "IN")
        self.assertEqual(parsed1.record_type, "A")
        self.assertEqual(parsed1.ip, "151.101.193.67")

        self.assertEqual(str(parsed1), "[name: cnn.com., ttl: 14, class=IN, type=A, ip=151.101.193.67]")

        line2 = "www.cnn.com.            261     IN      CNAME   turner-tls.map.fastly.net."
        parsed2 = DigSectionLine.parse(line2)
        self.assertEqual(parsed2.name, "www.cnn.com.")
        self.assertEqual(parsed2.ttl, 261)
        self.assertEqual(parsed2.response_class, "IN")
        self.assertEqual(parsed2.record_type, "CNAME")
        self.assertEqual(parsed2.ip, "turner-tls.map.fastly.net.")

        line3 = "turner-tls.map.fastly.net. 29   IN      A       151.101.1.67"
        parsed3 = DigSectionLine.parse(line3)
        self.assertEqual(parsed3.name, "turner-tls.map.fastly.net.")
        self.assertEqual(parsed3.ttl, 29)
        self.assertEqual(parsed3.response_class, "IN")
        self.assertEqual(parsed3.record_type, "A")
        self.assertEqual(parsed3.ip, "151.101.1.67")