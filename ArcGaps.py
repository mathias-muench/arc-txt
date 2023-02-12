import unittest
from Relations import Relations


class ArcGaps:
    def __init__(self, baseline: Relations, target: Relations):
        self.baseline = baseline
        self.target = target

    def gaps(self):
        b = set(self.baseline.used_sbbs())
        t = set(self.target.used_sbbs())
        return list(t - b)


class TestArcGaps(unittest.TestCase):
    baseline_rels = [
        {
            "SType": "Person",
            "SName": "sbb4",
            "DType": "System",
            "DName": "banking_system",
            "Label": "view_label1",
        }
    ]
    target_rels = [
        {
            "SType": "Person",
            "SName": "sbb4",
            "DType": "System",
            "DName": "banking_system",
            "Label": "view_label1",
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
        self.assertEqual(self.gaps.gaps(), [("System", "ATM")])
