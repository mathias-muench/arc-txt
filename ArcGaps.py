import unittest
from Relations import Relations


class ArcGaps:
    def __init__(self, baseline: Relations, target: Relations):
        self.baseline = baseline
        self.target = target

    def sbb_gaps(self):
        b = set(self.baseline.used_sbbs())
        t = set(self.target.used_sbbs())
        return list(t - b)

    def rel_gaps(self):
        b = set(self.baseline.rels)
        t = set(self.target.rels)
        return list(t - b)


class TestArcGaps(unittest.TestCase):
    baseline_rels = [
        {
            "SType": "Person",
            "SName": "sbb4",
            "DType": "System",
            "DName": "banking_system",
            "Label": "view_label1a",
        }
    ]
    target_rels = [
        {
            "SType": "Person",
            "SName": "sbb4",
            "DType": "System",
            "DName": "banking_system",
            "Label": "view_label1b",
        },
        {
            "SType": "Person",
            "SName": "sbb4",
            "DType": "System",
            "DName": "ATM",
            "Label": "view_label2",
        }
    ]

    def setUp(self):
        self.maxDiff = None
        baseline = Relations(__class__.baseline_rels)
        target = Relations(__class__.target_rels)
        self.gaps = ArcGaps(baseline, target)

    def test_gaps(self):
        self.assertEqual(self.gaps.sbb_gaps(), [("System", "ATM")])

    def test_rel_gaps(self):
        self.assertEqual(self.gaps.rel_gaps(), [
            {
                "SType": "Person",
                "SName": "sbb4",
                "DType": "System",
                "DName": "ATM",
                "Label": "view_label2",
            }
        ])
