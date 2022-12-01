# MIT License

# Copyright (c) 2018-2019 Groupe Allo-Media

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


"""
Test the ``text_to_num`` library.
"""
from unittest import TestCase
from text_to_num import alpha2digit, text2num


class TestTextToNumEN(TestCase):
    def test_text2num(self):
        test1 = "fifty-three billion two hundred forty-three thousand seven hundred twenty-four"
        self.assertEqual(text2num(test1, "en"), 53_000_243_724)

        test2 = (
            "fifty-one million five hundred seventy-eight thousand three hundred two"
        )
        self.assertEqual(text2num(test2, "en"), 51_578_302)

        test3 = "eighty-five"
        self.assertEqual(text2num(test3, "en"), 85)

        test4 = "eighty-one"
        self.assertEqual(text2num(test4, "en"), 81)

        self.assertEqual(text2num("fifteen", "en"), 15)
        self.assertEqual(text2num("hundred fifteen", "en"), 115)
        self.assertEqual(text2num("one hundred fifteen", "en"), 115)
        self.assertEqual(text2num("seventy-five thousands", "en"), 75000)
        self.assertEqual(text2num("thousand nine hundred twenty", "en"), 1920)
        
    def test_text2num_centuries(self):
        self.assertEqual(text2num("nineteen hundred seventy-three", "en"), 1973)

    def test_text2num_exc(self):
        self.assertRaises(ValueError, text2num, "thousand thousand two hundreds", "en")
        self.assertRaises(ValueError, text2num, "sixty fifteen", "en")

    def test_text2num_zeroes(self):
        self.assertEqual(text2num("zero", "en"), 0)
        self.assertEqual(text2num("zero eight", "en"), 8)
        self.assertEqual(text2num("zero zero hundred twenty five", "en"), 125)
        self.assertRaises(ValueError, text2num, "five zero", "en")
        self.assertRaises(ValueError, text2num, "fifty zero three", "en")
        self.assertRaises(ValueError, text2num, "fifty three zero", "en")

    def test_alpha2digit_integers(self):
        source = "twenty-five cows, twelve chickens and one hundred and twenty five kg of potatoes."
        expected = "25 cows, 12 chickens and 125 kg of potatoes."
        self.assertEqual(alpha2digit(source, "en"), expected)

        source = "one two three four twenty fifteen"
        expected = "1 2 3 4 20 15"
        self.assertEqual(alpha2digit(source, "en"), expected)

        source = "twenty-one, thirty-one."
        expected = "21, 31."
        self.assertEqual(alpha2digit(source, "en"), expected)

        # large number
        source = "fifty-three billion two hundred forty-three thousand seven hundred twenty-four"
        expected = "53,000,243,724"
        self.assertEqual(alpha2digit(source, "en"), expected)

    def test_hundred_multiplier_changes(self):
        self.assertEqual(text2num("sixty hundred", "en"), 6000)
        self.assertEqual(text2num("twenty two hundred", "en"), 2200)

        self.assertEqual(alpha2digit("thirty-three nine", "en"), "33 9")
        self.assertEqual(alpha2digit("plus thirty-three nine", "en"), "+33 9")
        self.assertEqual(alpha2digit("minus thirty-three nine", "en"), "-33 9")
        self.assertEqual(alpha2digit("thirty-three hundred", "en"), "3300")
        self.assertEqual(alpha2digit("thirty-three hundred one", "en"), "3301")
        self.assertEqual(alpha2digit("thirty-three hundred and one", "en"), "3301")
        self.assertEqual(alpha2digit("thirty-three hundred and one point five", "en"), "3301.5")
        self.assertEqual(alpha2digit("thirty-three and one point five", "en"), "33 and 1.5")
        self.assertEqual(alpha2digit("twenty one three", "en"), "21 3")

    def test_alpha2digit_formal(self):
        source = "plus thirty-three nine sixty zero six twelve twenty-one"
        expected = "+33 9 60 06 12 21"
        self.assertEqual(alpha2digit(source, "en"), expected)
        source = "plus thirty-three nine sixty o six twelve twenty-one"
        self.assertEqual(alpha2digit(source, "en"), expected)

        source = "zero nine sixty zero six twelve twenty-one"
        expected = "09 60 06 12 21"
        self.assertEqual(alpha2digit(source, "en"), expected)
        source = "o nine sixty o six twelve twenty-one"
        self.assertEqual(alpha2digit(source, "en"), expected)

        source = "My name is o s c a r."
        self.assertEqual(alpha2digit(source, "en"), source)

    def test_and(self):
        source = "fifty sixty thirty and eleven"
        expected = "50 60 30 and 11"
        self.assertEqual(alpha2digit(source, "en"), expected)

        self.assertEqual(alpha2digit("two thousand and four hundred", "en"), "2400")
        self.assertEqual(alpha2digit("two thousand and four hundred and five", "en"), "2405")
        self.assertEqual(alpha2digit("two thousand four hundred and five", "en"), "2405")

        self.assertEqual(alpha2digit("fourteen and five", "en"), "14 and 5")

    
    def test_currency(self):
        source = "one thousand two hundred sixty-six dollars."
        expected = "$1266."
        self.assertEqual(alpha2digit(source, "en"), expected)

        source = "one thousand point one USD"
        expected = "$1000.1"
        self.assertEqual(alpha2digit(source, "en"), expected)

        source = "one thousand euros in cash."
        expected = "€1000 in cash."
        self.assertEqual(alpha2digit(source, "en"), expected)

        source = "two euros."
        expected = "€2."
        self.assertEqual(alpha2digit(source, "en"), expected)

        source = "one euros."
        self.assertEqual(alpha2digit(source, "en"), source)

        source = "a million euros."
        self.assertEqual(alpha2digit(source, "en"), source)

    def test_alpha2digit_zero(self):
        source = "thirteen thousand zero ninety"
        expected = "13,000 090"
        self.assertEqual(alpha2digit(source, "en"), expected)
        source = "thirteen thousand o ninety"
        self.assertEqual(alpha2digit(source, "en"), expected)

        self.assertEqual(alpha2digit("zero", "en"), "0")

    def test_alpha2digit_ordinals(self):
        source = (
            "Fifth third second twenty-first hundredth one thousand two hundred thirtieth twenty-fifth thirty-eighth forty-ninth."
        )
        expected = "5th third second 21st 100th 1230th 25th 38th 49th."
        self.assertEqual(alpha2digit(source, "en"), expected)
        source = (
            "first, second, third, fourth, fifth, sixth, seventh, eighth, ninth, tenth."
        )
        expected = "first, second, third, 4th, 5th, 6th, 7th, 8th, 9th, 10th."
        self.assertEqual(alpha2digit(source, "en"), expected)

        source = "twenty second position at the twenty first event lost after the first second"
        expected = "22nd position at the 21st event lost after the first second"
        self.assertEqual(alpha2digit(source, "en"), expected)

    def test_alpha2digit_ordinals_force(self):
        source = (
            "first, second, third, fourth, fifth, sixth, seventh, eighth, ninth, tenth."
        )
        expected = "1st, 2nd, 3rd, 4th, 5th, 6th, 7th, 8th, 9th, 10th."
        self.assertEqual(alpha2digit(source, "en", ordinal_threshold=0), expected)

    def test_alpha2digit_decimals(self):
        source = (
            "twelve point ninety-nine, one hundred twenty point zero five,"
            " one hundred twenty point o five, one point two hundred thirty-six."
        )
        expected = "12.99, 120.05, 120.05, 1.236."
        self.assertEqual(alpha2digit(source, "en"), expected)

        self.assertEqual(alpha2digit("point fifteen", "en"), "0.15")
        self.assertEqual(alpha2digit("point one five", "en"), "0.15")
        self.assertEqual(alpha2digit("dot one five", "en"), "0.15")
        self.assertEqual(alpha2digit("twenty dot one five six", "en"), "20.15 6")

        self.assertEqual(alpha2digit("The average density is zero point five", "en"), "The average density is 0.5")
    
    def test_alpha2digit_dates(self):
        source = "May fifth twenty twelve"
        expected = "May 5th 20 12"
        self.assertEqual(alpha2digit(source, "en"), expected)

        source = "May five twenty one thirty"
        expected = "May 5 21 30"
        self.assertEqual(alpha2digit(source, "en"), expected)





    def test_alpha2digit_percent(self):
        self.assertEqual(alpha2digit("point fifteen percent", "en"), "0.15 %")
        self.assertEqual(alpha2digit("two hundred percent", "en"), "200 %")

    def test_alpha2digit_signed(self):
        source = "We have plus twenty degrees inside and minus fifteen outside."
        expected = "We have +20 degrees inside and -15 outside."
        self.assertEqual(alpha2digit(source, "en"), expected)

    def test_one_as_noun_or_article(self):
        source = "This is the one I'm looking for. One moment please! Twenty one cats. One two three four!"
        expected = "This is the one I'm looking for. One moment please! 21 cats. 1 2 3 4!"
        self.assertEqual(alpha2digit(source, "en"), expected)
        source = "No one is innocent. Another one bites the dust."
        self.assertEqual(alpha2digit(source, "en"), source)
        source = "one cannot know"
        self.assertEqual(alpha2digit(source, "en"), source)
        # End of segment
        source = "No one. Another one. One one. Twenty one"
        expected = "No one. Another one. 1 1. 21"
        self.assertEqual(alpha2digit(source, "en"), expected)

    def test_second_as_time_unit_vs_ordinal(self):
        source = "One second please! twenty second is parsed as twenty-second and is different from twenty seconds."
        expected = "One second please! 22nd is parsed as 22nd and is different from 20 seconds."
        self.assertEqual(alpha2digit(source, "en"), expected)

    def test_uppercase(self):
        source = "FIFTEEN ONE TEN ONE"
        expected = "15 1 10 1"
        self.assertEqual(alpha2digit(source, "en"), expected)
