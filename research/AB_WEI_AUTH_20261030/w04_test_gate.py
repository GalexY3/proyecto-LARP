#!/usr/bin/env python3
"""W04 frozen one-positive, six-negative fixture suite, NOT Wei samples."""
import unittest
from w04_quota_gate import QUOTAS, GateError, validate


def make_valid():
    rows = []
    for cls, count in enumerate(QUOTAS):
        for j in range(count):
            x = (cls * 137 + j * 37) % 997 / 997 * 20
            y = (cls * 211 + j * 113) % 991 / 991 * 20
            rows.append(f"{cls} {x:.12g} {y:.12g}")
    return rows


class ParityGateCases(unittest.TestCase):
    def test_valid_400(self):
        result = validate("\n".join(make_valid()) + "\n")
        self.assertEqual(result["n"], 400)
        self.assertEqual(result["quotas"], [163, 85, 68, 50, 34])

    def check_bad(self, mutation, code):
        lines = make_valid()
        mutation(lines)
        with self.assertRaises(GateError) as ctx:
            validate("\n".join(lines) + "\n")
        self.assertEqual(ctx.exception.code, code)

    def test_short_n(self):
        self.check_bad(lambda v: v.pop(), "N")

    def test_class_imbalance_same_n(self):
        self.check_bad(lambda v: v.__setitem__(0, "1 " + v[0].split(" ", 1)[1]), "QUOTA")

    def test_nan_coordinate(self):
        self.check_bad(lambda v: v.__setitem__(0, "0 nan 1"), "NONFINITE")

    def test_out_of_bounds(self):
        self.check_bad(lambda v: v.__setitem__(0, "0 20 1"), "BOUNDS")

    def test_illegal_class(self):
        self.check_bad(lambda v: v.__setitem__(0, "5 1 1"), "CLASS")

    def test_bad_column_count(self):
        self.check_bad(lambda v: v.__setitem__(0, "0 1"), "FORMAT")


if __name__ == "__main__":
    unittest.main(verbosity=2)
