import unittest
from capacity import reserve, release

class CapacityTests(unittest.TestCase):
    def test_reserve_below_capacity(self):
        self.assertEqual(reserve(2, 3, 8), 5)

    def test_reserve_exact_fill_from_zero(self):
        result = reserve(0, 1, 1)
        self.assertIs(type(result), int)
        self.assertEqual(result, 1)

    def test_reserve_exact_fill_from_partial_usage(self):
        result = reserve(2, 3, 5)
        self.assertIs(type(result), int)
        self.assertEqual(result, 5)

    def test_reject_over_capacity(self):
        with self.assertRaises(ValueError): reserve(6, 3, 8)

    def test_release_some(self):
        self.assertEqual(release(5, 2), 3)

    def test_release_all(self):
        self.assertEqual(release(5, 5), 0)

    def test_reject_over_release(self):
        with self.assertRaises(ValueError): release(3, 4)

if __name__ == '__main__': unittest.main()
