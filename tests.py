import unittest
from scrape_fv import normalize_value, normalize_key


class RegexTests(unittest.TestCase):
    def test_blank(self):
        self.assertEqual(normalize_value("-"), None)

    def test_percents(self):
        self.assertEqual(normalize_value("21.50%"), .215)
        self.assertEqual(normalize_value("0.01%"), .0001)
        self.assertEqual(normalize_value("-1.42%"), -.0142)
        self.assertEqual(normalize_value("102.49%"), 1.0249)

    def test_decimals(self):
        self.assertEqual(normalize_value("60.20"), 60.2)
        self.assertEqual(normalize_value("3.0"), 3)
        self.assertEqual(normalize_value("0.01"), .01)
        self.assertEqual(normalize_value("-20.2"), -20.2)

    def test_letter_abreviated_numbers(self):
        self.assertEqual(normalize_value("2.86T"), 2860000000000)
        self.assertEqual(normalize_value("1032.35B"), 1032350000000)
        self.assertEqual(normalize_value("53.26B"), 53260000000)
        self.assertEqual(normalize_value("-2.22B"), -2220000000)
        self.assertEqual(normalize_value("10.00M"), 10000000)
        self.assertEqual(normalize_value("-1.09M"), -1090000)
        self.assertEqual(normalize_value("109.00K"), 109000)
        self.assertEqual(normalize_value("1.10K"), 1100)
        self.assertEqual(normalize_value("-221.14K"), -221140)

    def test_plain_ints(self):
        self.assertEqual(normalize_value("1"), 1)
        self.assertEqual(normalize_value("104233923400"), 104233923400)
        self.assertEqual(normalize_value("-23324"), -23324)

    def test_comma_separated_ints(self):
        self.assertEqual(normalize_value("123,152,423"), 123152423)
        self.assertEqual(normalize_value("1,234"), 1234)
        self.assertEqual(normalize_value("-2,642,035,934"), -2642035934)

    def test_booleans(self):
        self.assertEqual(normalize_value("Yes"), True)
        self.assertEqual(normalize_value("No"), False)

    def test_all_other(self):
        self.assertEqual(normalize_value("m02x39ri3029rfh"), "m02x39ri3029rfh")


if __name__ == '__main__':
    unittest.main()
