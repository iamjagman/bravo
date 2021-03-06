# vim: set fileencoding=utf8 :

import unittest

from numpy import array

import bravo.utilities

class TestCoordHandling(unittest.TestCase):

    def test_split_coords(self):
        cases = {
            (0, 0): (0, 0, 0, 0),
            (1, 1): (0, 1, 0, 1),
            (16, 16): (1, 0, 1, 0),
            (-1, -1): (-1, 15, -1, 15),
            (-16, -16): (-1, 0, -1, 0),
        }
        for x, z in cases:
            self.assertEqual(bravo.utilities.split_coords(x, z), cases[x, z])

class TestBitTwiddling(unittest.TestCase):

    def test_unpack_nibbles(self):
        self.assertEqual(bravo.utilities.unpack_nibbles(["a"]), [1, 6])
        self.assertEqual(bravo.utilities.unpack_nibbles("nibbles"),
            [14, 6, 9, 6, 2, 6, 2, 6, 12, 6, 5, 6, 3, 7])

    def test_pack_nibbles(self):
        self.assertEqual(bravo.utilities.pack_nibbles(array([1, 6])), "a")
        self.assertEqual(
            bravo.utilities.pack_nibbles(array([14, 6, 9, 6, 2, 6, 3, 7])),
            "nibs")

    def test_nibble_reflexivity(self):
        self.assertEqual("nibbles",
            bravo.utilities.pack_nibbles(
                array(bravo.utilities.unpack_nibbles("nibbles"))
            )
        )

class TestStringMunging(unittest.TestCase):

    def test_sanitize_chat_color_control_at_end(self):
        message = u"§0Test§f"
        sanitized = u"§0Test"
        self.assertEqual(bravo.utilities.sanitize_chat(message), sanitized)

class TestNumberMunching(unittest.TestCase):

    def test_split_time(self):
        # Sunrise.
        self.assertEqual(bravo.utilities.split_time(0), (6, 0))
        # Noon.
        self.assertEqual(bravo.utilities.split_time(6000), (12, 0))
        # Sunset.
        self.assertEqual(bravo.utilities.split_time(12000), (18, 0))
        # Midnight.
        self.assertEqual(bravo.utilities.split_time(18000), (0, 0))
