import unittest
from Relations import Relations


class ArcGaps:
    def __init__(self, baseline: Relations, target: Relations):
        self.baseline = baseline
        self.target = target

    def sbb_gaps(self) -> set:
        b = set(self.baseline.used_sbbs())
        t = set(self.target.used_sbbs())
        return t - b

    def rel_gaps(self) -> set:
        b = set(self.baseline.rels)
        t = set(self.target.rels)
        return t - b


class TestArcGaps(unittest.TestCase):
    baseline_rels = [
        {
            "Source": "Person:sbb4:>0",
            "Destination": "System:banking_system:>0",
            "Label": "view_label1a",
        }
    ]
    target_rels = [
        {
            "Source": "Person:sbb4:>0",
            "Destination": "System:banking_system:>1",
            "Label": "view_label1b",
        },
        {
            "Source": "Person:sbb4:>0",
            "Destination": "System:ATM:>0",
            "Label": "view_label2",
        },
    ]

    def setUp(self):
        self.maxDiff = None
        baseline = Relations(__class__.baseline_rels)
        target = Relations(__class__.target_rels)
        self.gaps = ArcGaps(baseline, target)

    def test_sbb_gaps(self):
        self.assertSetEqual(
            self.gaps.sbb_gaps(),
            set([("System", "ATM", ">0"), ("System", "banking_system", ">1")]),
        )

    def test_rel_gaps(self):
        self.assertSetEqual(
            self.gaps.rel_gaps(),
            set(
                [
                    (("Person", "sbb4", ">0"), ("System", "ATM", ">0")),
                    (("Person", "sbb4", ">0"), ("System", "banking_system", ">1")),
                ]
            ),
        )
