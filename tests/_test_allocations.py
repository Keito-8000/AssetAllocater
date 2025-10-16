import unittest
from core.asset import Assets
from core.allocation import Allocation
from core.allocations import Allocations


class TestAssetsAndAllocations(unittest.TestCase):

    def setUp(self):
        # Example base assets
        self.assets = Assets({
            "US Stock": 50000,
            "Bond": 30000,
            "Cash": 20000
        })

        # Example allocation scenarios
        self.alloc1 = Allocation({"US Stock": 0.6, "Bond": 0.3, "Cash": 0.1})
        self.alloc2 = Allocation({"US Stock": 0.4, "Bond": 0.4, "Cash": 0.2})

        self.allocations = Allocations([self.alloc1, self.alloc2])

    def test_allocation_total_ratio(self):
        self.assertAlmostEqual(self.alloc1.total_ratio(), 1.0)
        self.assertAlmostEqual(self.alloc2.total_ratio(), 1.0)

    def test_allocations_normalize(self):
        a = Allocation({"US Stock": 60, "Bond": 30, "Cash": 10})
        allocs = Allocations([a])
        allocs.normalize()
        self.assertAlmostEqual(a.total_ratio(), 1.0)

    def test_assets_total(self):
        total = self.assets.total()
        self.assertEqual(total, 100000)

    def test_multiplication_single_allocation(self):
        # Multiply with single allocation
        result = self.assets * Allocations([self.alloc1])
        expected = {
            "US Stock": 50000 * 0.6,
            "Bond": 30000 * 0.3,
            "Cash": 20000 * 0.1
        }
        for k, v in expected.items():
            self.assertAlmostEqual(result.values[k], v)

    def test_multiplication_multiple_allocations(self):
        # Multiply with multiple allocations (last one applied)
        result = self.assets * self.allocations
        expected = {
            "US Stock": 50000 * 0.4,
            "Bond": 30000 * 0.4,
            "Cash": 20000 * 0.2
        }
        for k, v in expected.items():
            self.assertAlmostEqual(result.values[k], v)


if __name__ == "__main__":
    unittest.main()
